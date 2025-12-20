---
title: Spotify   Genres Network Analysis
published: true
date: 2021-12-18 03:28:33 UTC
tags: medium,blog,python
canonical_url: https://medium.com/p/3047c5b9b777
---

# Spotify — Genres Network Analysis

Spotify is the largest music streaming service in the world serving more than 381 million users in over 180+ countries around the world… 

* * *

### Spotify — Genres Network Analysis

Spotify is the largest music streaming service in the world serving more than [381 million users](https://www.statista.com/statistics/367739/spotify-global-mau/) in over [180+ countries](https://support.spotify.com/us/article/where-spotify-is-available/) around the world. with millions of active users, and a huge variety of music genres, Spotify creates a great database that I was interested to explore.

I was curious to see if by creating a genres network I could find a correlation between the number of artists playing a genre to its betweenness centrality in the network.  
To do so, I gathered the data using [Spotify API](https://developer.spotify.com/documentation/web-api/) and “[Spotipy](https://spotipy.readthedocs.io/en/2.19.0/)” Python library. I used the [ORA network software](https://netanomics.com/ora-commercial-version/) to analyze and visualize the data.

**Collecting Data**

The Spotify genres couldn’t all be pulled at once. Therefore, I collected all 1256 playlists from the [Spotify official](https://open.spotify.com/user/spotify?si=055269231ff94a99&nd=1) account. The reason I chose to use the official Spotify account playlists is the lack of influence by a particular genre, a particular era, or a certain country.

For every song in the playlists, I took its artist, then for every artist I used the ‘[related-artist](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-related-artists)’ function on Spotify API which gave me 20 more related artists to each one of the artists on my list. This step allowed me to expand my dataset. The next step was to determine how many artists shared the same genre duo. Through the Spotify API, I gathered information on each artist’s related genres. These 1937 genres were inputted into a matrix.

**Network Analysis**

Using the matrix I built, I created the genres network. My approach was to create a genre-based network in which every node consists of one musical genre. The edge weight is the number of artists who play both genres.

![](https://cdn-images-1.medium.com/max/2560/1*O-UNhWx1otwXJ7coPwSd4g.png)Left- Genres Network Graph, Bode Color by Louvain Algorithm. Right- Zoom In

I discovered that the number of artists related to a genre is distributed in a power-law distribution. This means that a few genres are played by a lot of artists, while many other genres are played by a fewer number of artists.

Among all genres, Rock, Dance-Pop, and Classic-Rock have the largest number of musicians who played those genres.

![](https://cdn-images-1.medium.com/max/800/1*jUlsShPG8rsaVaxL7gSBSA.png)

Dance-Pop, Pop, and Pop-Rap for example, had the larger [betweenness](https://www.sci.unich.it/~francesc/teaching/network/betweeness.html#:~:text=Betweenness%20centrality%20measures%20the%20extent,over%20information%20passing%20between%20others) rate (Normalized betweenness measures how often one node acts as a bridge between two other nodes).

![](https://cdn-images-1.medium.com/max/800/1*2nZzQo5lOV9dUhDBnRULJg.png)

**Conclusion**

In the linear line function, the X axis represents the degree betweenness of a genre. The Y axis represents the total degree of a genre.

![](https://cdn-images-1.medium.com/max/800/1*sxAukeJVMIF5vS7Mk4JGyA.png)

The coefficient of determination is 0.4, which indicates a low positive correlation. It shows that when more artists play a genre, that genre will have more connections with other genres in the network.

**Final Notes**

This was my first attempt to understand and analyze a data network. As an active Spotify user, I enjoyed learning about Spotify’s genre network Since the platform gives a lot of data from many perspectives. I feel that I have only touched the tip of the iceberg.

Contact me : [Gmail](mailto:kfir.gisman@gmail.com) [GitHub](http://bit.ly/37C0vth) [LinkedIn](http://bit.ly/2VMjsaf)

By [Kfir Gisman](https://medium.com/@Kfir-G) on [December 18, 2021](https://medium.com/p/3047c5b9b777).

[Canonical link](https://medium.com/@Kfir-G/spotify-genres-network-analysis-3047c5b9b777)

Exported from [Medium](https://medium.com) on December 20, 2025.
