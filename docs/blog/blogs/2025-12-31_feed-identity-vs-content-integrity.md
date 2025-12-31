---
title: Appendix - Feed Identity vs Content Integrity
published: true
date: 2025-12-31 00:00:00 UTC
tags: podcasts,security,rss,feed,provenance
canonical_url: https://kfir-g.dev/blog/blogs/2025-12-31_feed-identity-vs-content-integrity
---

# Appendix: Feed Identity vs Content Integrity

This appendix complements [my article on Podcast Security](https://kfir-g.dev/blog/blogs/2025-12-30_podcasts-as-a-supply-chain-missing-security-model/).

---

Podcast security can be thought of in two complementary layers:

## 1. Content Integrity
- Guarantees that the audio file delivered to a listener is exactly the same as the one published.
- Traditionally involves cryptographic hashes, signatures, and immutability.
- **Challenges in podcasting:**
  - Dynamic ad insertion (different regions get different audio)
  - CDN variations and caching
  - Personalized content or regional versions
- **Result:** A canonical audio artifact often **does not exist**, making episode-level integrity hard to enforce.

## 2. Feed Identity / Provenance
- Ensures that a listener or app discovers the authoritative feed for a given show.
- Focuses on trusting the source, rather than each audio file:
  - Prevents copied or fake feeds from masquerading as the original show
  - Reduces the risk of monetization or ad tampering on duplicate feeds
- **Feeds act as the primary security anchor, while content may vary dynamically.**
- **Key insight:** In today’s ecosystem, establishing feed identity may provide more practical security guarantees than attempting per-episode integrity. Feed-level trust enables listeners and apps to rely on the original publisher, even when audio content is personalized or region-specific.
- **Platform-agnostic:** This concept applies regardless of hosting or playback platform.

## Visual Diagram

```text
                 +--------------------------+           +--------------------------+
                 |      Podcast Feed        |           |      Podcast Feed        |
                 |      (Original)          |           |      (Original)          |
                 +-----------+--------------+           +-----------+--------------+
                             |                                      |
                -------------------------------          ------------------------------
                |  Listener / App receives    |          | Listener / App receives    |
                |  audio with integrity?      |          | audio may vary per region, |
                |  (same file for everyone)   |          | dynamic ads, CDN, etc.     |
                -------------------------------          ------------------------------
                    Content Integrity                          Feed Identity
```

**Takeaway:**

* **Content Integrity:** Audio may differ per listener due to ads, CDN, region, or personalization.
* **Feed Identity:** Ensures the listener reaches the correct authoritative feed, even if the audio varies dynamically.
