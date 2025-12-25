---
title: Why You Should Disable Cloud Storage Bucket Versioning
published: true
date: 2023-08-23 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/e6638beffac6
---

# Why You Should Disable Cloud Storage Bucket Versioning

Cloud Storage is a service that allows you to store and access your data on Google’s infrastructure. It offers high availability… 

* * *

### Why You Should Disable Cloud Storage Bucket Versioning

Cloud Storage is a service that allows you to store and access your data on Google’s infrastructure. It offers high availability, durability, scalability, and performance for your data. One of the features that Cloud Storage provides is Bucket Versioning, which lets you keep multiple versions of an object in the same bucket. This can be useful for recovering from accidental deletions or overwrites, as well as preserving historical versions of your data. However, in this blog post, I will explain why you might want to disable Cloud Storage Bucket Versioning, and how to do it.

### The Drawbacks of Cloud Storage Bucket Versioning

While Cloud Storage Bucket Versioning can have some benefits, it also comes with some drawbacks that you should be aware of. Here are some of the reasons why you might want to disable Cloud Storage Bucket Versioning:

  * **Cost** : Each version of an object is charged at the same rate as when it was live, so keeping multiple versions can increase your storage costs. You can use Object Lifecycle Management to delete older versions automatically, but this may not be sufficient for your needs. For example, if you have a large number of objects that change frequently, you might end up with a lot of versions that you don’t need. Moreover, if you enable Bucket Versioning on a bucket that already contains objects, all the existing objects will be treated as live versions, and you will be charged for them as well.
  * **Complexity** : Managing multiple versions of an object can add complexity to your application logic and workflows. You need to specify the generation number of the version you want to access, and handle cases where there are no live or noncurrent versions available. For example, if you want to list all the objects in a bucket, you need to use the `versions` parameter to include both live and noncurrent versions, or use the `prefixes` parameter to group them by name. If you want to download or delete an object, you need to use the `generation` parameter to specify which version you want. If you don’t specify a generation number, Cloud Storage will use the latest live version by default.
  * **Security** : If you have sensitive data that you want to delete permanently, disabling Cloud Storage Bucket Versioning can ensure that no traces of the data remain in the bucket. Otherwise, you need to delete each version individually by specifying the generation number, or use Object Lifecycle Management to delete them after a certain period of time. However, this may not be enough to guarantee that your data is completely erased from Google’s servers. According to Google’s [documentation](https://cloud.google.com/storage/docs/object-versioning#permanently_delete)\- Google may retain deleted versions for some time after deletion and those deleted versions may still be accessible by authorized users until they are permanently erased. Therefore, if you want to avoid any potential risks of data leakage or breach, disabling Cloud Storage Bucket Versioning might be a better option.



### How to Disable Cloud Storage Bucket Versioning

If you decide that Cloud Storage Bucket Versioning is not suitable for your needs, you can disable it easily using one of the following methods:

**Google Cloud Console** : You can use the Google Cloud Console to manage your buckets and objects. To disable Cloud Storage Bucket Versioning for a bucket, follow these steps:

  1. Go to the [Cloud Storage Browser] page in the Google Cloud Console.
  2. Select the bucket that you want to disable Cloud Storage Bucket Versioning for.
  3. Click on the **Edit bucket** button at the top of the page.
  4. Under the **Versioning** section, uncheck the box next to **Enable versioning**.
  5. Click on **Save** to apply the changes.



**gsutil** : You can use the gsutil command-line tool to perform various operations on your buckets and objects. To disable Cloud Storage Bucket Versioning for a bucket, use this command:
    
    
    gsutil versioning set off gs://<bucket_name>

Replace `<bucket_name>` with the name of your bucket.

**Cloud Storage API** : You can use the Cloud Storage API to programmatically interact with your buckets and objects. To disable Cloud Storage Bucket Versioning for a bucket, send a PATCH request to this endpoint:
    
    
    PATCH https://storage.googleapis.com/storage/v1/b/<bucket_name>

Replace `bucket_name` with the name of your bucket. In the request body, set the `versioning.enabled` property to `false`. For example:
    
    
    {  
      "versioning": {  
        "enabled": false  
      }  
    }

**Terraform** :
    
    
    resource "google_storage_bucket" "bucket_name" {  
      ...  
      versioning {  
        enabled = false  
      }  
    }

### Conclusion

Cloud Storage Bucket Versioning is a feature that can help you preserve and restore multiple versions of your objects in the same bucket. However, it also has some drawbacks that might outweigh its benefits, such as cost, complexity, and security. Therefore, you might want to disable Cloud Storage Bucket Versioning for your buckets, depending on your use case and requirements. You can use the Google Cloud Console, the gsutil command-line tool, or the Cloud Storage API to disable Cloud Storage Bucket Versioning easily and quickly.

* * *

### **References**

  1. <https://cloud.google.com/storage/docs/using-versioned-objects>
  2. <https://cloud.google.com/storage/docs/object-versioning#permanently_delete>
  3. <https://cloud.google.com/storage/docs/samples/storage-disable-versioning>
  4. <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket#enabled>



By [Kfir Gisman](https://medium.com/@Kfir-G) on [August 23, 2023](https://medium.com/p/e6638beffac6).

[Canonical link](https://medium.com/@Kfir-G/why-you-should-disable-cloud-storage-bucket-versioning-e6638beffac6)
