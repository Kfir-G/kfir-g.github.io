---
title: Spotify  Genres Network Analysis By Through Decades
published: true
date: 2022-03-20 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/b7d325f9677a
---

# Spotify- Genres Network Analysis by Through Decades

In my last story, “Spotify — Genres Network Analysis”, I felt I had only begun to explore Spotify genres network. As a fan of certain… 

* * *

### **Spotify- Genres Network Analysis by Through Decades**

In my last story, “[ _Spotify — Genres Network Analysis_](https://medium.com/@kfir_g/spotify-genres-network-analysis-3047c5b9b777)”, I felt I had only begun to explore Spotify genres network. As a fan of certain music genres, I wondered what their role was throughout the decades in terms of popularity. I was especially curious about the popularity and the importance of pop and rock in the years of 1960–2020.

### **The Data**

To answer my question, I needed to collect all the genres in Spotify. It was not possible to pull all Spotify genres simultaneously. I instead collected all 1256 [_Spotify official_](https://open.spotify.com/user/spotify?si=4112c72be73f4e15) __ playlists with [_Spotify API_](https://developer.spotify.com/documentation/web-api/). Every song on the playlist I labelled according to the decade it belongs to by the song's field "[_release_date_](https://developer.spotify.com/console/get-track/)". This gave me a table of songs for each decade. Further, I pulled out the genre for every track and finally I made a table of genres for each decade. ([_link to the python file_](https://github.com/Kfir-G/Spotify-Decades-Analysis/blob/main/SpotifyDecade.ipynb))

I modelled each decade table as a social network, with each node representing a musical genre. The edge weight represents the number of artists that played both genres.

The networks that came out were:  
60’s: 297 nodes with 4248 links.  
70’s: 422 nodes with 6330 links.  
80’s: 609 nodes with 8378 links.  
90’s: 1114 nodes with 15900 links.  
2000s: 1726 nodes with 25902 links.  
2010s: 1909 nodes with 38912 links.  
2020s: 1897 nodes with 31840 links.

![An example of the 60’s Network:](https://cdn-images-1.medium.com/max/800/1*oBWY_x_yyDbldQ_jNqb-Fg.png)An example of the 60’s Network

Finally, I combined all the decades’ networks into [_one dynamic social network_](https://github.com/Kfir-G/Spotify-Decades-Analysis/blob/main/Dynamic%20Network-Spotify-Decades.xml.xml) __ that allowed me to see the genres through a timeline.

* * *

### **Findings**

For an analysis of the relative importance of a genre over decades, I used the measure of [_betweenness_](https://www.sci.unich.it/~francesc/teaching/network/betweeness.html#:~:text=Betweenness%20centrality%20measures%20the%20extent,over%20information%20passing%20between%20others) __ that gave me a relative score of the genre. Based on this score, I could tell whether the genre was largely important and popular.

![](https://cdn-images-1.medium.com/max/800/1*RIC40UQN_hACpT9pWMyopQ.png)The Betweenness Graph of The Pop and Rock Genres

According to this graph, the Rock reached its peak in the 1980s and then began to decline. Meanwhile, Pop has grown rapidly starting to gain its popularity around 1980s.

### **Conclusions**

In the 1980’s, the peak of the betweenness graph correlates with the high rate of rock songs released in the following graph. On both graphs, the peaks appear in the late 1970’s and at the beginning of the 1980's.

![](https://cdn-images-1.medium.com/max/800/1*EQ75KjnZ_Nlsp9uprU6Hmw.png)Graph by “[ _FiveThirtyEight_](https://fivethirtyeight.com/features/why-classic-rock-isnt-what-it-used-to-be/)”

Based on the data presented in [_“The date face”_](https://thedataface.com/2016/09/culture/genre-lifecycles) (shown below), the pop genre became popular in the 1980’s and soared to popularity in the start of the 2000’s. This information correlates with the betweenness graph, which demonstrate that pop became extremely popular and focal in the beginning of the 2000's.

![](https://cdn-images-1.medium.com/max/800/1*8mqv-VkkUyBJ38QAgrq7yQ.png)

* * *

> Thanks to [Omer](https://github.com/omer3020) and [Mahdi](https://github.com/silvamod) for helped me gather the data.

Contact Me: [Github](https://github.com/Kfir-G)

By [Kfir Gisman](https://medium.com/@Kfir-G) on [March 20, 2022](https://medium.com/p/b7d325f9677a).

[Canonical link](https://medium.com/@Kfir-G/spotify-genres-network-analysis-by-through-decades-b7d325f9677a)
