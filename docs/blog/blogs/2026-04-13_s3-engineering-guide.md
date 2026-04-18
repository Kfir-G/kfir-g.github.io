---
title: Stop Using upload_file()- S3 Engineering for High-Throughput Systems
published: true
date: 2026-04-13 00:00:00 UTC
tags: python, aws, s3, performance, asyncio, engineering
canonical_url: https://kfir-g.dev/blog/blogs/2026-04-10_s3-engineering-guide
---

# Beyond `upload_file()`: How to Handle S3 Like a True Engineer

Most developers treat Amazon S3 like a magic folder. They call `s3.upload_file()`, hope for the best, and move on. But when you’re building high-throughput systems, "hoping for the best" leads to OOM (Out of Memory) kills and corrupted data.

After digging deep into the AWS documentation and battle-testing my FastAPI services, I’ve refined a strategy for S3 that prioritizes memory efficiency, data integrity, and non-blocking I/O.

### **1. The Memory Problem: Streaming in Chunks**
Loading a 2GB file into RAM to upload it is a beginner's mistake. A true engineer streams data. By using a chunked approach, your memory usage stays flat whether the file is 10MB or 10GB.

### **2. Integrity: Server-Side MD5 Verification**
How do you know the bytes that left your NIC are exactly what arrived at Amazon? You don’t-unless you use the `Content-MD5` header. By calculating the MD5 hash locally and sending it with the request, S3 will reject the upload if even a single bit is flipped during transit.

### **3. The Async Bottleneck: Don't Block the Loop**
`boto3` is a synchronous library. If you call it directly inside an `async def` FastAPI route, you stop the entire event loop. To stay asynchronous, you must offload the work to a **ThreadPoolExecutor** or use a native async library like `aioboto3`.

### **4. Latency, Jitter, and Metadata**
Network calls fail. Engineers implement **Exponential Backoff + Jitter** to prevent crashing services during recovery. Additionally, we use **Metadata** to store context (like uploader IDs), saving us from expensive database lookups later.

### **The "Engineer's Choice" Implementation**

Here is a robust pseudo code, asynchronous wrapper for the standard `boto3` client that ensures your FastAPI server stays responsive while maintaining data integrity.

```python
# --- THE ENGINEER'S BLUEPRINT (PSEUDO-CODE) ---

async def upload_file_engineered(path, bucket, key):
    # 1. SETUP: Configure standard retries with jitter + timeouts
    s3_client = initialize_client(retries=5, backoff="exponential_with_jitter")
    
    # 2. INTEGRITY: Stream file through MD5 to keep RAM footprint low
    # We do this before uploading to ensure we know exactly what we are sending
    md5_hash = new_hasher("md5")
    with open(path, "rb") as stream:
        while chunk := stream.read(4096):
            md5_hash.update(chunk)
    
    encoded_md5 = base64_encode(md5_hash.digest())

    # 3. ASYNC WRAPPER: S3 calls are usually blocking (sync)
    # To prevent freezing the main Event Loop, we offload to a thread
    async with open(path, "rb") as file_data:
        upload_task = lambda: s3_client.put_object(
            target=bucket,
            name=key,
            payload=file_data,       # Streams directly from disk
            checksum=encoded_md5,    # S3 will verify this on their end
            metadata={"user": "kfir"} # Meaningful context
        )

        try:
            # 4. EXECUTION: Run the sync task in a non-blocking thread pool
            result = await run_in_background_thread(upload_task)
            return result
            
        except IntegrityError:
            # 5. ERROR HANDLING: Catch if a single bit flipped during transit
            log_critical("Data corruption detected! Local MD5 != S3 MD5")
            raise
```

### **Conclusion**
Reading the documentation isn't just about finding the right function; it's about understanding the **contract** between your code and the infrastructure. 

By handling chunks, verifying hashes, and managing the event loop correctly, you aren't just moving files-you're building a resilient system that won't fail when the load gets heavy.

**Next time you hit S3, ask yourself: Is this just an upload, or is this engineering?**

---

## References:
https://docs.aws.amazon.com/boto3/latest/reference/services/s3/bucket/put_object.html <br/>
https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html <br/>
https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html <br/>
