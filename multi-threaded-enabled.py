from pytube import Playlist, YouTube
from multiprocessing.pool import ThreadPool as Pool
import timeit


#for multi-threading of playlist downloding
pool_size = 10
def worker(video):
    print("Downloading", video.title)
    video.streams.get_by_itag(22).download()
    print("Download comleted", video.title, "\n")
pool = Pool(pool_size)

def video_downloader(url):
    vid = YouTube(url)
    #print("\nDownloading", vid.title)
    vid.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    print("Download comleted", vid.title, "\n")

def playlist_downloader(url):
    playlst = Playlist(url)
    print(f'***********\nDownloading: {playlst.title}\n***********\n')
    for video in playlst.videos:
        pool.apply_async(worker, (video,))
    pool.close()
    pool.join()
        

def func_completion():
    print("\n************\nTask completed\n************\n")
    url = input("Enter URL: ")
    main_func(url)    

def main_func(url):
    try:    
        try:
            video_downloader(url)
            func_completion()
        except:
            start = timeit.default_timer()
            playlist_downloader(url)
            func_completion()
            stop = timeit.default_timer()
            print('Time: ', stop - start)
    except Exception as e: 
        print(e, "\n\n")
        main_func(url)

url = input("Enter URL: ")
main_func(url)
