# pyMovieRenamer
A python script for renaming movie folders and files. Makes filenames and folders readable!

Instructions:
Install python
Place the movierename.py and wordlist.txt in the root of your folder where you keep your movies. For it to work, your root should contain seperate folders, with videofiles and subtitle files in them. 

Example input and output:  
this.movie.is.cool.2021.1080p.bluray.rip/ -> This Movie Is Cool (2021)/  
this.movie.is.cool.2021.1080p.bluray.rip.mkv -> This Movie Is Cool (2021).mkv  
this.movie.is.cool.2021.1080p.bluray.rip.srt -> This Movie Is Cool (2021).srt  
      
this.movie.is.also.cool.2020.1080p.bluray.rip/ -> This Movie Is Also Cool (2020)/  
this.movie.is.also.cool.2020.1080p.bluray.rip.avi -> This movie Is Also Cool (2020).avi  
this.movie.is.also.cool.2020.1080p.bluray.rip.srt -> This Movie Is Also Cool (2020).srt    
  
Movie without year 10bit hevc bluray 1080p.mkv -> Movie Without Year.mkv   
