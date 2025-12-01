---
title: "Episode 1 - Ssali Jonathan"
date: 2025-11-30
tags: [podcast, software, dev]
audio: "/podcast/audio-files/episode1-jod35.mp3"
---

<img src="/podcast/logo.png" alt="Code with Mate Logo" width="200"/>

# Episode 1 - Ssali Jonathan

<div id="podcast-player">
    <audio id="episode-audio" controls style="width: 100%;">
      <source src="/podcast/audio-files/episode1-jod35.mp3" type="audio/mpeg">
      <source src="/podcast/audio-files/episode1-jod35.mp3" type="audio/mp3">
      Your browser does not support the audio element.
    </audio>
</div>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        const audio = document.getElementById('episode-audio');

        // Check for decoding errors after the file attempts to load metadata
        audio.addEventListener('error', (e) => {
            const error = audio.error;
            let message = '';
            
            // Code 4 is MEDIA_ERR_SRC_NOT_SUPPORTED (which includes decoding errors)
            if (error && error.code === error.MEDIA_ERR_SRC_NOT_SUPPORTED) {
                message = 'The media resource could not be decoded. (MIME/Header Error)';
            } else if (error) {
                message = `Media error code: ${error.code} (Check console for NS_ERROR_DOM_MEDIA_METADATA_ERR)`;
            }

            if (message) {
                console.error("Audio Playback Failed:", message);
                
                // CRITICAL WORKAROUND: Force a specific source change to trigger reload
                audio.pause();
                audio.src = '/podcast/audio-files/episode1-jod35.mp3';
                audio.load();
                console.log('Attempting second load with forced source.');
            }
        });
        
        // Try to load the audio immediately
        audio.load();
    });
</script>

Episode 1 kicks off with Ssali Jonathan — software engineer and open-source enthusiast. We talk about his journey in tech, his content creation, and Python web frameworks. A relaxed, honest conversation about building, learning, and growing in software - with mate on the side.

**Topics we cover:** <br/>
- Exploring Python web frameworks.<br/>
- Diving into FastAPI and Starlette.<br/>
- Database choices and real-world experiences.<br/>
- Redis beyond a simple key-value store.<br/>
- Learning and growth as a software engineer.<br/>

**Connect with Ssali Jonathan:** <br/>
- GitHub: [https://github.com/jod35](https://github.com/jod35)  
- Website: [https://jod35.github.io/site/](https://jod35.github.io/site/)  
- YouTube: [https://www.youtube.com/@SsaliJonathan](https://www.youtube.com/@SsaliJonathan)  
- Twitter (X): [https://twitter.com/jod35_](https://twitter.com/jod35_)
