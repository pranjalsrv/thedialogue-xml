import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import xml.etree.ElementTree as etree
from email import utils

cred = credentials.Certificate('service-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

blogs_ref = db.collection(u'blogs').order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(10)
docs = blogs_ref.stream()


class Item:
    title = ""
    description = ""
    link = ""
    guid = ""
    pubDate = ""
    image = ""

    def __init__(self, doc):
        blog_dict = doc.to_dict()
        self.title = blog_dict['title']
        self.description = blog_dict['description']
        self.link = "https://thedialogue.co.in/article/" + doc.id
        self.guid = "https://thedialogue.co.in/article/" + doc.id
        self.pubDate = utils.format_datetime(blog_dict['timestamp'])
        self.image = blog_dict['image']

    def get_item_xml(self):
        item = etree.Element("item")

        title = etree.SubElement(item, "title")
        title.text = self.title

        description = etree.SubElement(item, "description")
        description.text = self.description

        link = etree.SubElement(item, "link")
        link.text = self.link

        guid = etree.SubElement(item, "guid")
        guid.text = self.guid

        pubDate = etree.SubElement(item, "pubDate")
        pubDate.text = self.pubDate

        image = etree.SubElement(item, "image")
        image.text = self.image

        return item


tree = etree.parse("rss.xml")
channel = tree.find('channel')

for doc in docs:
    blog_item = Item(doc=doc)
    guid_list = [guid.text for guid in tree.iter('guid')]
    if blog_item.guid not in guid_list:
        channel.append(blog_item.get_item_xml())

tree.write('rss.xml')
