import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def scraper(url, resp):
    links = extract_next_links(url, resp)
    file2 = open("links.txt", "a")
    for link in links:
        if is_valid(link):
            file2.write(link + '\n')

    return [link for link in links if is_valid(link)]


# cd spacetime-crawler4py-master
# python launch.py --restart
# python launch.py

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    result = set()  # 存储结果, remove duplicates

    file1 = open("contents.txt", "a")
    if url.is_redirected:
        pass
    if is_valid(url) and resp.status == 200:
        mypage = BeautifulSoup(resp.raw_response.content, 'html.parser')

        try:
            for link in mypage.find_all('a'):
                hyperlink = link.get('href')
                if is_valid(hyperlink):
                    defragement = hyperlink.split('#')[0].split('?')[0]
                    result.add(defragement)
                    # file2.write(defragement + '\n')

            content = mypage.get_text()
            file1.write(content.strip() + '\n')
        except AttributeError:
            pass
        except TypeError:
            pass

    return list(result)


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if 'events' in url:  # trap?????????????
            return False
        if 'mailto' in url:  # trap?????
            return False
        # below are changed
        if ".ics.uci.edu" in parsed.hostname or \
                ".cs.uci.edu" in parsed.hostname or \
                ".informatics.uci.edu" in parsed.hostname or \
                ".stat.uci.edu" in parsed.hostname or \
                ".today.uci.edu/department/information_computer_sciences" in parsed.hostname:
            if not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
                return True
            else:
                return False
        else:
            return False

    except TypeError:
        print("TypeError for ", parsed)
        raise
