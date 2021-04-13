import os
import shutil
from bs4 import BeautifulSoup
import csv

origin_path = "/home/sarita/Documents/CS584/Takeout/Voice/Calls"
dest_path = "/home/sarita/Documents/CS584/rechatbot/data"

for filename in os.listdir(origin_path):
    if "Text" in filename and filename.endswith("html"):
        shutil.copy(os.path.join(origin_path, filename), os.path.join(dest_path, filename))


with open('data/messages.csv', mode='w') as messages_file:
    messages_writer = csv.writer(messages_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    seen_contacts = set()
    for filename in sorted(os.listdir(dest_path)):

        contact = filename.split('-')[0].strip()
        if contact in seen_contacts or not contact.startswith("+"):
            continue
        else:
            seen_contacts.add(contact)

            with open(os.path.join(dest_path, filename)) as html_file:
                contents = html_file.read()
                soup = BeautifulSoup(contents, 'html')
                for tag in soup.findAll('q'):
                    print(tag.text)
                    messages_writer.writerow([tag.text])
    

    messages_file.close()