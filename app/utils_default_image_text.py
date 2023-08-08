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


EMAIL_COPY_TEXT_0 = """Dear customer,\n
We hope this email finds you well.\n
We're writing to let you know about our upcoming sale on new women's handbags at Cymbal. We're offering discounts of up to 50% on all items, so this is a great opportunity to stock up on some new handbags for yourself or for someone special.\n
We have a wide variety of handbags to choose from, including totes, satchels, crossbody bags, and more. We also have a variety of colors and styles to choose from, so you're sure to find something that you love.\n
Our sale starts on Friday, March 11th and ends on Sunday, March 13th. So be sure to shop early to get the best selection.\n
To take advantage of our sale, simply visit our website at www.cymbal.com and enter the code "SALE50" at checkout.\n
We hope to see you soon!\n
Sincerely,\n
The Cymbal Team"""

EMAIL_COPY_TEXT_1 = """Dear customer,\n
We're excited to introduce our new line of men's shoes at Cymbal. We know you'll love the stylish designs and comfortable construction.\n
Our new shoes are perfect for men of all ages, including middle-aged men like you. They're made with high-quality materials and construction, so you can be sure they'll last.\n
We also have a variety of styles to choose from, so you're sure to find the perfect pair of shoes for your needs. Whether you're looking for a pair of dress shoes for work or a pair of casual shoes for weekend wear, we have something for you.\n
To celebrate the launch of our new line of men's shoes, we're offering a special discount of 20% off your first purchase. Just use the code NEWLINE at checkout.\n
So what are you waiting for? Shop our new line of men's shoes today.\n
Sincerely,\n
The Cymbal Team"""

EMAIL_COPY_TEXT_2 = """Dear customer,\n
We're excited to announce the new opening of Cymbal concept shoe store in New York City! We know you're a middle-aged man, so we think you'd really appreciate our unique selection of shoes.\n
Cymbal is a new concept store that offers a curated selection of shoes from around the world. We have something for everyone, whether you're looking for a new pair of sneakers, sandals, or boots.\n
We're also offering a special discount to our first 100 customers. Use the code "NEWCYMBAL" at checkout to save 20% on your purchase.\n
We hope to see you soon at Cymbal!\n
Sincerely,\n
The Cymbal Team"""

EMAIL_COPY_TEXT_3 = """Dear customer,\n
We hope this email finds you well.\n
We're reaching out to you today because we know you're a fan of Cymbal shoes, and we wanted to let you know that we're now open in New York City!\n
We're located at 123 Main Street, and we're open from 10am to 6pm, seven days a week.\n
We have a wide selection of Cymbal shoes to choose from, including our latest styles and designs. We also have a variety of sizes and widths to choose from, so you're sure to find the perfect pair of shoes for you.\n
In addition to our shoes, we also have a variety of other Cymbal merchandise, including t-shirts, hats, and bags.\n
We hope you'll stop by and visit us soon!\n
Sincerely,\n
The Cymbal Team"""


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


AUDIENCE_QUERY_0 = """SELECT c.email, SUM(t.transaction_value) as total_transaction_value
FROM `rl-llm-dev.cdp_dataset.customers` as c
JOIN `rl-llm-dev.cdp_dataset.transactions` as t
ON c.customer_id = t.customer_id
WHERE c.city = "New York City"
GROUP BY c.email, c.city
ORDER BY total_transaction_value DESC"""

AUDIENCE_QUERY_1 = """SELECT c.city, c.state, SUM(t.transaction_qnt) as total_transactions
FROM `rl-llm-dev.cdp_dataset.customers` as c
JOIN `rl-llm-dev.cdp_dataset.transactions` as t
ON c.customer_id = t.customer_id
GROUP BY c.city, c.state
ORDER BY total_transactions DESC
LIMIT 1"""

AUDIENCE_QUERY_2 = """SELECT c.email
FROM `rl-llm-dev.cdp_dataset.customers` as c
ORDER BY c.loyalty_score DESC
LIMIT 50"""


AUDIENCE_RESULT_0 = {'email': {0: 'user36410@sample_user36410.sample',
  1: 'user39537@sample_user39537.sample',
  2: 'user42905@sample_user42905.sample',
  3: 'user16185@sample_user16185.sample',
  4: 'user27153@sample_user27153.sample',
  5: 'user38115@sample_user38115.sample',
  6: 'user10294@sample_user10294.sample',
  7: 'user14325@sample_user14325.sample',
  8: 'user11798@sample_user11798.sample',
  9: 'user3917@sample_user3917.sample',
  10: 'user7486@sample_user7486.sample',
  11: 'user654@sample_user654.sample',
  12: 'user8239@sample_user8239.sample',
  13: 'user27383@sample_user27383.sample',
  14: 'user16127@sample_user16127.sample',
  15: 'user6385@sample_user6385.sample',
  16: 'user14330@sample_user14330.sample',
  17: 'user17562@sample_user17562.sample',
  18: 'user40714@sample_user40714.sample',
  19: 'user25908@sample_user25908.sample',
  20: 'user22574@sample_user22574.sample',
  21: 'user44252@sample_user44252.sample',
  22: 'user34710@sample_user34710.sample',
  23: 'user40677@sample_user40677.sample',
  24: 'user4400@sample_user4400.sample',
  25: 'user17852@sample_user17852.sample',
  26: 'user40544@sample_user40544.sample',
  27: 'user48183@sample_user48183.sample',
  28: 'user6405@sample_user6405.sample',
  29: 'user17702@sample_user17702.sample',
  30: 'user9840@sample_user9840.sample',
  31: 'user31034@sample_user31034.sample',
  32: 'user19437@sample_user19437.sample',
  33: 'user21268@sample_user21268.sample',
  34: 'user27294@sample_user27294.sample',
  35: 'user42572@sample_user42572.sample',
  36: 'user28448@sample_user28448.sample',
  37: 'user26172@sample_user26172.sample',
  38: 'user26013@sample_user26013.sample',
  39: 'user42867@sample_user42867.sample',
  40: 'user4667@sample_user4667.sample',
  41: 'user23411@sample_user23411.sample',
  42: 'user11656@sample_user11656.sample',
  43: 'user25866@sample_user25866.sample',
  44: 'user49602@sample_user49602.sample',
  45: 'user19915@sample_user19915.sample',
  46: 'user42246@sample_user42246.sample',
  47: 'user592@sample_user592.sample',
  48: 'user47535@sample_user47535.sample',
  49: 'user21012@sample_user21012.sample',
  50: 'user5975@sample_user5975.sample',
  51: 'user5649@sample_user5649.sample',
  52: 'user37969@sample_user37969.sample',
  53: 'user10005@sample_user10005.sample',
  54: 'user8546@sample_user8546.sample',
  55: 'user44610@sample_user44610.sample',
  56: 'user34455@sample_user34455.sample',
  57: 'user18936@sample_user18936.sample',
  58: 'user49902@sample_user49902.sample',
  59: 'user48833@sample_user48833.sample',
  60: 'user35410@sample_user35410.sample',
  61: 'user39020@sample_user39020.sample',
  62: 'user28768@sample_user28768.sample',
  63: 'user1125@sample_user1125.sample',
  64: 'user19287@sample_user19287.sample',
  65: 'user39590@sample_user39590.sample',
  66: 'user44117@sample_user44117.sample',
  67: 'user12706@sample_user12706.sample',
  68: 'user1924@sample_user1924.sample',
  69: 'user37719@sample_user37719.sample',
  70: 'user14927@sample_user14927.sample',
  71: 'user17747@sample_user17747.sample',
  72: 'user6976@sample_user6976.sample',
  73: 'user33807@sample_user33807.sample',
  74: 'user27189@sample_user27189.sample',
  75: 'user19130@sample_user19130.sample',
  76: 'user2779@sample_user2779.sample',
  77: 'user40625@sample_user40625.sample',
  78: 'user15806@sample_user15806.sample',
  79: 'user18432@sample_user18432.sample',
  80: 'user24894@sample_user24894.sample',
  81: 'user20643@sample_user20643.sample',
  82: 'user36840@sample_user36840.sample',
  83: 'user15752@sample_user15752.sample',
  84: 'user8421@sample_user8421.sample',
  85: 'user2693@sample_user2693.sample',
  86: 'user42475@sample_user42475.sample',
  87: 'user28549@sample_user28549.sample',
  88: 'user43513@sample_user43513.sample',
  89: 'user15311@sample_user15311.sample',
  90: 'user28935@sample_user28935.sample',
  91: 'user17628@sample_user17628.sample',
  92: 'user16924@sample_user16924.sample',
  93: 'user4683@sample_user4683.sample',
  94: 'user9467@sample_user9467.sample',
  95: 'user30496@sample_user30496.sample',
  96: 'user31249@sample_user31249.sample',
  97: 'user13864@sample_user13864.sample'},
 'total_transaction_value': {0: 855492,
  1: 852387,
  2: 843707,
  3: 821528,
  4: 732435,
  5: 726079,
  6: 703611,
  7: 695777,
  8: 636451,
  9: 628616,
  10: 628538,
  11: 627163,
  12: 598239,
  13: 588209,
  14: 580621,
  15: 550972,
  16: 540952,
  17: 533339,
  18: 505052,
  19: 498978,
  20: 492421,
  21: 487951,
  22: 485941,
  23: 472743,
  24: 464157,
  25: 446107,
  26: 443166,
  27: 432757,
  28: 415912,
  29: 401274,
  30: 398301,
  31: 375952,
  32: 370532,
  33: 363755,
  34: 356996,
  35: 350192,
  36: 349640,
  37: 330854,
  38: 321455,
  39: 319205,
  40: 315922,
  41: 305209,
  42: 304387,
  43: 300598,
  44: 298813,
  45: 296925,
  46: 296791,
  47: 280331,
  48: 270050,
  49: 268125,
  50: 266801,
  51: 265422,
  52: 261508,
  53: 245947,
  54: 239911,
  55: 239701,
  56: 229055,
  57: 227826,
  58: 226913,
  59: 225748,
  60: 222330,
  61: 218379,
  62: 217244,
  63: 202029,
  64: 198744,
  65: 196405,
  66: 188142,
  67: 184548,
  68: 178732,
  69: 178075,
  70: 162264,
  71: 161908,
  72: 160442,
  73: 148332,
  74: 148025,
  75: 136272,
  76: 130051,
  77: 126735,
  78: 117824,
  79: 115718,
  80: 115377,
  81: 113887,
  82: 110341,
  83: 105452,
  84: 103384,
  85: 99592,
  86: 99154,
  87: 98176,
  88: 94938,
  89: 92404,
  90: 84311,
  91: 83096,
  92: 59097,
  93: 53123,
  94: 44095,
  95: 31759,
  96: 27079,
  97: 10910}}


AUDIENCE_RESULT_1 = {'city': {0: 'Atlanta'},
 'state': {0: 'Georgia'},
 'total_transactions': {0: 252986}}

AUDIENCE_RESULT_2 = {'email': {0: 'user23270@sample_user23270.sample',
  1: 'user24288@sample_user24288.sample',
  2: 'user38207@sample_user38207.sample',
  3: 'user745@sample_user745.sample',
  4: 'user25690@sample_user25690.sample',
  5: 'user30279@sample_user30279.sample',
  6: 'user35966@sample_user35966.sample',
  7: 'user43789@sample_user43789.sample',
  8: 'user4074@sample_user4074.sample',
  9: 'user43233@sample_user43233.sample',
  10: 'user6176@sample_user6176.sample',
  11: 'user12726@sample_user12726.sample',
  12: 'user3250@sample_user3250.sample',
  13: 'user33932@sample_user33932.sample',
  14: 'user32664@sample_user32664.sample',
  15: 'user46052@sample_user46052.sample',
  16: 'user33480@sample_user33480.sample',
  17: 'user11535@sample_user11535.sample',
  18: 'user30778@sample_user30778.sample',
  19: 'user43266@sample_user43266.sample',
  20: 'user27647@sample_user27647.sample',
  21: 'user11880@sample_user11880.sample',
  22: 'user22675@sample_user22675.sample',
  23: 'user42238@sample_user42238.sample',
  24: 'user38678@sample_user38678.sample',
  25: 'user1667@sample_user1667.sample',
  26: 'user29133@sample_user29133.sample',
  27: 'user23415@sample_user23415.sample',
  28: 'user9307@sample_user9307.sample',
  29: 'user34107@sample_user34107.sample',
  30: 'user22474@sample_user22474.sample',
  31: 'user27639@sample_user27639.sample',
  32: 'user3407@sample_user3407.sample',
  33: 'user6225@sample_user6225.sample',
  34: 'user12341@sample_user12341.sample',
  35: 'user44287@sample_user44287.sample',
  36: 'user40735@sample_user40735.sample',
  37: 'user21005@sample_user21005.sample',
  38: 'user5473@sample_user5473.sample',
  39: 'user28258@sample_user28258.sample',
  40: 'user29831@sample_user29831.sample',
  41: 'user44710@sample_user44710.sample',
  42: 'user41217@sample_user41217.sample',
  43: 'user10756@sample_user10756.sample',
  44: 'user39478@sample_user39478.sample',
  45: 'user20887@sample_user20887.sample',
  46: 'user9105@sample_user9105.sample',
  47: 'user19446@sample_user19446.sample',
  48: 'user31778@sample_user31778.sample',
  49: 'user8725@sample_user8725.sample'}}