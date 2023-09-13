# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from io import BytesIO
import io
import streamlit as st


def get_default_image_bytesio(
        image_path: str,
        selected_image_key: str,
        display_image: bool = False) -> BytesIO:
    with open(image_path, 'rb') as fp:
        image = io.BytesIO(fp.read())
    st.session_state[selected_image_key] = image
    if display_image:
        st.write("**Currently select image:**")
        st.image(image)


DEFAULT_EMAIL_TEXT = """Dear customer,\n
We hope this email finds you well.\n
We're writing to let you know about our upcoming sale on new handbags and shoes at Cymbal. We're offering discounts on all items, so this is a great opportunity to stock up on some new pieces for your wardrobe.\n
We have a wide variety of handbags to choose from, including totes, satchels, crossbody bags, and more. We also have a variety of styles to choose from, so you're sure to find something that you love.\n
Our shoes are made from high-quality materials and construction, so you can be sure that they'll last for years to come.\n
To take advantage of this sale, simply visit our website at www.cymbal.com and enter the code SAVE50 at checkout. Don't miss out!\n
We hope to see you soon at Cymbal!\n
Sincerely,\n
The Cymbal Team"""

WEBSITE_TEXT_WOMEN_HANDBAG = """New Women's Handbags on Sale at Cymbal\n
Cymbal is excited to announce the arrival of our new collection of women's handbags. These stylish and functional bags are perfect for any occasion, from a night out on the town to a day at the office.\n
Our new handbags come in a variety of styles, colors, and sizes to suit your individual needs. Whether you're looking for a small crossbody bag to carry your essentials or a large tote bag for work, we have something for you.\n
In addition to our wide selection of styles, our new handbags are also made from high-quality materials that will last for years to come. We use only the finest leathers and fabrics, so you can be sure that your new bag will look and feel great for years to come.\n
We're also offering a special sale on our new handbags. You can save on select styles, so don't miss out on this opportunity to stock up on your new favorite bag.\n
Shop our new collection of women's handbags today and find the perfect bag to complete your look.\n
Here are some of our top picks from the new collection:\n
The Cymbal Tote Bag is a stylish and spacious bag that's perfect for everyday use. It features a roomy interior with multiple compartments, so you can keep your belongings organized. The Cymbal Tote Bag is also made from durable leather that will last for years to come.\n
The Cymbal Crossbody Bag is a chic and compact bag that's perfect for a night out on the town. It features a stylish design and a comfortable crossbody strap, so you can wear it all day long. The Cymbal Crossbody Bag is also made from lightweight leather that won't weigh you down.\n
The Cymbal Satchel Bag is a versatile and stylish bag that can be dressed up or down. It features a sleek design and a spacious interior, so you can carry everything you need. The Cymbal Satchel Bag is also made from durable leather that will last for years to come.\n
These are just a few of our top picks from the new collection of women's handbags at Cymbal. Shop our entire collection today and find the perfect bag to complete your look."""

WEBSITE_TEXT_MEN_SHOES = """Introducing the New Line of Men's Shoes at Cymbal\n
We're excited to announce the launch of our new line of men's shoes! We've been working hard to create a collection that is stylish, comfortable, and durable, and we think you're going to love it.\n
Our new line features a variety of styles to suit every man's needs. Whether you're looking for a pair of dress shoes for work, casual shoes for everyday wear, or athletic shoes for your next workout, we have something for you.\n
We've also used only the finest materials in our construction, so you can be sure that our shoes will last. And because we know that life happens, all of our shoes come with a 90-day warranty.\n
So what are you waiting for? Check out our new line of men's shoes today!\n
Here are just a few of the features of our new line of men's shoes:\n
 - Stylish designs that will turn heads\n
 - Comfortable construction that will keep you feeling your best all day long\n
 - Durable materials that will last for years to come\n
 - A 90-day warranty that gives you peace of mind\n
We're confident that you'll love our new line of men's shoes. So what are you waiting for? Shop now!\n
Here are some of the styles that are available in our new line of men's shoes:\n
 - Dress shoes\n
 - Casual shoes\n
 - Athletic shoes\n
 - Boots\n
 - Sandals\n
We have something for every man, so be sure to check out our entire collection today!\n
We're also offering a special discount of 20% off your first purchase. Just use the code NEWLINE at checkout.\n
So what are you waiting for? Shop now and start looking your best!"""

WEBSITE_TEXT_CONCEPT_STORE = """Cymbal Concept Shoe Store Opens in NYC\n
New York City, NY – March 8, 2023 – Cymbal, a new concept shoe store, opened its doors in New York City today. The store, located at 100 Fifth Avenue, offers a unique shopping experience that combines the latest in fashion with cutting-edge technology.\n
Cymbal is the brainchild of two friends, Ben and Jerry. Ben is a former footwear designer who worked for some of the biggest brands in the industry. Jerry is a tech entrepreneur who has developed a new platform that allows shoppers to interact with products in a whole new way.\n
The store is divided into two sections. The first section is dedicated to the latest in fashion. Cymbal carries a wide variety of shoes from both established brands and up-and-coming designers. The second section is where the technology comes in.\n
Cymbal has developed a platform that allows shoppers to interact with products in a virtual environment. Using the platform, shoppers can try on shoes, change colors, and even see how they would look on different body types.\n
The platform is also integrated with social media, allowing shoppers to share their experiences with friends and family.\n
Cymbal is the first store of its kind in the world. It offers a unique shopping experience that is sure to appeal to both fashion-forward shoppers and tech-savvy consumers.\n
About Cymbal\n
Cymbal is a new concept shoe store that combines the latest in fashion with cutting-edge technology. The store, located at 100 Fifth Avenue in New York City, offers a unique shopping experience that allows shoppers to interact with products in a virtual environment.\n
Cymbal was founded by two friends, Ben and Jerry. Ben is a former footwear designer who worked for some of the biggest brands in the industry. Jerry is a tech entrepreneur who has developed a new platform that allows shoppers to interact with products in a whole new way.\n
Cymbal carries a wide variety of shoes from both established brands and up-and-coming designers. The store also offers a variety of services, including shoe repair and customization.\n
Cymbal is the future of shoe shopping. It is a place where fashion and technology meet to create an unforgettable shopping experience.\n
To learn more about Cymbal, visit their website at www.cymbal.com."""

WEBSITE_TEXT_BRAND = """Cymbal Shoes: A New Retail Brand in NYC\n
Cymbal Shoes is a new retail brand that is taking the city by storm. With its unique selection of shoes, stylish designs, and affordable prices, Cymbal Shoes is quickly becoming a go-to destination for shoe lovers of all ages.\n
Cymbal Shoes was founded by two friends who had a passion for shoes and a desire to create a brand that was different from anything else on the market. They wanted to create a brand that was stylish, affordable, and accessible to everyone.\n
Cymbal Shoes offers a wide variety of shoes, including sneakers, boots, sandals, and heels. They also have a variety of styles to choose from, including casual, dressy, and athletic. And with prices starting at just $20, Cymbal Shoes is sure to have something for everyone.\n
In addition to their wide selection of shoes, Cymbal Shoes also offers a variety of other services, such as free shipping and returns, and a 30-day satisfaction guarantee.\n
Cymbal Shoes is located in the heart of New York City, at 123 Main Street. They are open seven days a week, from 10am to 8pm.\n
If you're looking for a new pair of shoes, be sure to check out Cymbal Shoes. You won't be disappointed!\n
Here are some of the reasons why Cymbal Shoes is a great choice:\n
 - Unique selection of shoes\n
 - Stylish designs\n
 - Affordable prices\n
 - Free shipping and returns\n
 - 30-day satisfaction guarantee\n
 - Convenient location\n
If you're looking for a new pair of shoes, be sure to check out Cymbal Shoes. You won't be disappointed!"""


ASSET_GROUP_HEADLINES = """Cymbal: New Women's Handbags.\n
Shop the Latest Handbag Collection at Cymbal.\n
Cymbal: Chic Handbags for Every Occasion.\n
Cymbal: Elevate Your Style with a New Handbag.\n
Cymbal: A New Handbag for Every Woman."""

ASSET_GROUP_LONG_HEADLINES = """Cymbal: A symphony of style. Elevate your look with our new collection of women's handbags.\n
Cymbal: Timeless elegance and modern style. Discover our new collection of women's handbags.\n
Cymbal: The perfect handbag for every occasion. Shop our latest collection now.\n
Cymbal: Chic, stylish, and sophisticated. Our new collection of women's handbags is sure to turn heads.\n
Cymbal: A new season, a new you. Shop our latest collection of women's handbags and start your new year off in style."""

ASSET_GROUP_DESCRIPTION = "Cymbal's new collection of women's handbags is a symphony of style, featuring a harmonious blend of trendsetting designs and unparalleled quality."


SOCIAL_THREADS_0 = """New handbags at Cymbal!\n
Looking for a new handbag to add to your collection? Look no further than Cymbal! We have a wide variety of handbags to choose from, all at great prices. Whether you're looking for a stylish crossbody bag, a roomy tote bag, or a chic clutch, we have something for everyone.\n
And now, for a limited time, take an extra 20% off all handbags! This is the perfect opportunity to stock up on your favorite styles or treat yourself to a new bag."""

SOCIAL_THREADS_1 = """Introducing the new line of shoes from Cymbal!\n
Our new line of shoes is perfect for the modern woman on the go. With a variety of styles to choose from, you're sure to find the perfect pair of shoes to match your personality and lifestyle.\n
Our shoes are made with high-quality materials and construction, so you can be sure they'll last. Plus, they're incredibly comfortable, so you can wear them all day long.\n
So what are you waiting for? Shop our new line of shoes today!"""

SOCIAL_THREADS_2 = """Introducing Cymbal, a new concept shoe store in NYC.\n
Cymbal is a one-of-a-kind shoe store that offers a unique shopping experience. We have a wide selection of shoes from all the top brands, but what really sets us apart is our personal touch.\n
Our team of experts is here to help you find the perfect pair of shoes for your needs. We'll take the time to learn about your style and your lifestyle, and then we'll make recommendations that are perfect for you."""

SOCIAL_THREADS_3 = """Cymbal Shoes: The Perfect Shoes for Your Next Adventure\n
Looking for a pair of shoes that can keep up with your active lifestyle? Look no further than Cymbal Shoes! Our shoes are made with high-quality materials and construction, so you can be sure they'll last. Plus, our shoes are designed with comfort in mind, so you can wear them all day long.\n
Whether you're running errands, going to the gym, or just taking a walk around the city, Cymbal Shoes are the perfect choice for you. """

SOCIAL_INSTAGRAM_0 = """Cymbal is excited to announce the launch of our new line of handbags. These stylish and functional bags are perfect for any occasion, from a night out on the town to a day at the office.\n
Our handbags are made with high-quality materials and construction, so you can be sure they'll last. They're also available in a variety of colors and styles, so you're sure to find the perfect one for you.\n
To celebrate the launch of our new handbags, we're offering 20 percent off all purchases. So what are you waiting for? Shop now and get your new Cymbal handbag!\n
Shop now at cymbal.com."""

SOCIAL_INSTAGRAM_1 = """Introducing the new line of shoes from Cymbal!\n
Our new line of shoes is designed to take you from day to night, with styles that are both stylish and comfortable. Whether you're running errands, going to work, or out on the town, our shoes will have you looking and feeling your best.\n
Our new line of shoes features:\n
 - A variety of styles to choose from, including flats, heels, boots, and sandals\n
 - Comfortable, supportive soles that will keep you feeling your best all day long\n
 - Durable materials that will last season after season\n
 - Fashion-forward designs that will turn heads wherever you go\n
Shop our new line of shoes today and experience the difference!\n
Visit our website or find a store near you to see our full selection.\n
Cymbal: Shoes that make you feel good."""

SOCIAL_INSTAGRAM_2 = """Cymbal: The New Concept Shoe Store in NYC\n
Cymbal is a new concept shoe store that's unlike anything you've seen before. We offer a curated selection of the latest and greatest shoes from around the world, all at an affordable price.\n
We believe that shoes should be more than just a way to get from point A to point B. They should be an expression of your personality and style. That's why we offer a wide variety of styles to choose from, so you can find the perfect pair of shoes to match your look.\n
In addition to our amazing selection of shoes, we also offer a unique shopping experience. Our stores are designed to be inviting and inspiring, and our staff is always happy to help you find the perfect pair of shoes.\n
So if you're looking for a new pair of shoes that will make you stand out from the crowd, come check out Cymbal today!\n
Visit our website or stop by one of our stores today to find the perfect pair of shoes!"""

SOCIAL_INSTAGRAM_3 = """Cymbal Shoes: The Perfect Shoes for Your Next Adventure\n
Are you looking for the perfect shoes for your next adventure? Look no further than Cymbal Shoes! Our shoes are made with high-quality materials and construction, so you can be sure they'll last. Plus, our shoes are stylish and comfortable, so you can look and feel your best on your next big trip.\n
Whether you're hiking in the mountains, exploring a new city, or just running errands, Cymbal Shoes have you covered. Check out our wide selection of styles and colors today!\n
Shop now at cymbalshoes.com.\n
Cymbal Shoes: The perfect shoes for your next adventure."""
