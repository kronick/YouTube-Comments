import os
import sys
import urllib
import codecs
from bs4 import BeautifulSoup

#COMMENT_API = "https://gdata.youtube.com/feeds/api/videos/%s/comments?max-results=50&start-index=%i"

COMMENT_API = "http://www.youtube.com/all_comments?v=%s&page=%i"

def comments_for_video(video_id):
  page = 1
  found = 0

  out = codecs.open("%s.txt" % video_id, encoding='utf-16', mode='w')

  while True:
    url = COMMENT_API % (video_id, page)
    soup = BeautifulSoup(urllib.urlopen(url))

    comments = soup.select(".comment-body")
    for comment in comments:
      try:
        comment_text = comment.select(".comment-text")[0].get_text()
        comment_user = comment.select(".yt-user-name")[0].get_text()
        comment_time = comment.select(".time")[0].get_text()
	text = "%s (%s):\n%s\n\n--\n" % (comment_user.strip(), comment_time.strip(), comment_text.strip())

        print text
        out.write(text)
        #out.write("\n---\n")
      except:
        pass
    
    if len(comments) == 0:
      break

    found += len(comments)
    page += 1

  out.close()
  
  os.system("iconv -f utf-16 -t utf-8 %s.txt | sed -e ':a;N;$!ba;s#\\n(Show the comment)\s*\\n\s*# #g' -e 's#in reply to\s*#in reply to #g' > tmp; mv tmp %s.txt;" % (video_id, video_id))

  print "%i comments found." % found

def main():
  comments_for_video(sys.argv[1])

if __name__ == "__main__":
  main()
