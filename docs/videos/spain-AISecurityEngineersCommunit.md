# Beyond Prompt Injection: Breaking AI Agents via Low-Level Host Injections

I gave my second security talk. And I deliberately picked a bug that has absolutely nothing to do with jailbreaks, prompt injection, or anything you'd normally associate with "AI security."

Because here's the thing everyone keeps forgetting: an AI agent is still just code running on a normal web server. And normal web servers can be broken with normal web bugs - no clever prompt required.

This is the story of one of those bugs.

<iframe width="560" height="315"
        src="https://www.youtube.com/embed/w6_GKgjkk90"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen>
</iframe>

## Why you should care even if you've never heard of Starlette

FastAPI is built on top of Starlette. Starlette is the async engine underneath a huge chunk of the Python AI world - vLLM, LiteLLM, and LangChain's own deployment tool LangServe all expose their APIs directly on it. According to GitHub's Octoverse 2025 report, over 1.1 million public repos now use some LLM SDK, up 178% year over year.

So when a bug shows up in this specific layer, it's not some obscure edge case. It's sitting under the floorboards of a huge slice of production AI infrastructure - including yours, probably.

CVE-2026-48710, nicknamed "BadHost," was found by security firm X41 D-Sec while they were doing a paid security audit of vLLM, funded by OSTIF. Not fuzzing some random package - auditing one of the most widely deployed LLM-serving engines on the planet. That's part of why this one is worth paying attention to.

## The bug, in one paragraph

Starlette keeps two different versions of a request's path floating around at the same time, and they don't always agree.

* `scope["path"]` - parsed exactly once, straight off the socket. Immutable. This is what the router actually uses to decide where your request goes.
* `request.url.path` - rebuilt from scratch every time you touch it, by gluing together the scheme, the path, and the Host header - which the client controls.

Guess which one most authorization middleware actually checks? Yep. The one an attacker can influence.

## Watch it break in real time

Send a Host header like target.com/?, and Python's URL parser does exactly what it's supposed to do: treats everything after the ? as a query string, not a path. The reconstructed path collapses down to nothing - but the router underneath is still happily dispatching to the real, protected endpoint.

```python
# Vulnerable
if request.url.path.startswith("/admin"):
    return Forbidden()

# Fixed
if request.scope["path"].startswith("/admin"):
    return Forbidden()
```

Here it is in the terminal:
```bash
$ curl -i http://localhost:8080/admin/potato
HTTP/1.1 403 Forbidden

$ curl -i -H "Host: localhost:8080/?" http://localhost:8080/admin/potato
HTTP/1.1 200 OK   # bypassed
```

Same target route. Same server. The only thing that changed is one header. That's the whole exploit.

## "Just update the library" won't save you

I wish it were that simple. Starlette 1.0.1+ patches this for code paths that go through Starlette's own logic - but if your own middleware manually parses request.url anywhere, you're still exposed, no matter what version you're running. Upgrading a dependency fixes a bug in the library. It does not fix an architectural assumption baked into your own code.

The real fix is boring, in the best way: read from the raw ASGI scope, not a reconstructed convenience object. Layer that with defense-in-depth - strip malformed Host headers at the proxy/CDN, turn on TrustedHostMiddleware with an explicit allow-list, and move authorization onto signed tokens instead of string path matching.

## The point of all this

You cannot protect the weights inside a model if the web server wrapping them is already broken. AI security starts with AppSec - not the other way around. Don't let the hype around prompt injection make you forget the fundamentals.

---

**Slides:** [kfir-g.dev/assets/slides-BeyondPromptInjection.pdf](https://kfir-g.dev/assets/slides-BeyondPromptInjection.pdf)

<iframe src="https://kfir-g.dev/assets/slides-BeyondPromptInjection.pdf" width="100%" height="600px"></iframe>

## References

**The vulnerability:**

- Official advisory (GHSA-86qp-5c8j-p5mr) - [github.com/Kludex/starlette/security/advisories/GHSA-86qp-5c8j-p5mr](https://github.com/Kludex/starlette/security/advisories/GHSA-86qp-5c8j-p5mr)
- The fix (PR #3279) - [github.com/Kludex/starlette/pull/3279](https://github.com/Kludex/starlette/pull/3279)
- OSTIF disclosure writeup - [ostif.org/disclosing-the-badhost-vulnerability-in-starlette](https://ostif.org/disclosing-the-badhost-vulnerability-in-starlette/)
- Free scanner + Semgrep/CodeQL rules - [badhost.org](https://badhost.org)
- Additional technical write-up - [marcelotryle.com/blog/badhost-cve-2026-48710/#thank-you](https://marcelotryle.com/blog/badhost-cve-2026-48710/#thank-you)
- URI syntax background (RFC-level reference) - [en.wikipedia.org/wiki/Uniform_Resource_Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)

**Why this stack matters:**

- GitHub Octoverse 2025 - [github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- JetBrains, "Best Python AI Frameworks in 2026" - [blog.jetbrains.com/pycharm/2026/06/best-python-ai-frameworks-in-2026](https://blog.jetbrains.com/pycharm/2026/06/best-python-ai-frameworks-in-2026/)

**Mitigations mentioned in the talk:**

- Starlette `TrustedHostMiddleware` - [starlette.dev/middleware/#trustedhostmiddleware](https://www.starlette.io/middleware/#trustedhostmiddleware)
- Starlette `BaseHTTPMiddleware` - [starlette.dev/middleware/#basehttpmiddleware](https://www.starlette.io/middleware/#basehttpmiddleware)
- Cloudflare Transform Rules - [developers.cloudflare.com/rules/transform](https://developers.cloudflare.com/rules/transform/)
- Nginx Host header / `if` directive reference - [nginx.org/en/docs/http/ngx_http_core_module.html#var_host](https://nginx.org/en/docs/http/ngx_http_core_module.html#var_host) *(updated to official Nginx documentation)*

---

Special thanks to [Antonio Juanilla AkA Specter](https://www.linkedin.com/in/spectertj/) and [Francisco Arencibia Quesada](https://www.linkedin.com/in/franciscoarencibia/)
