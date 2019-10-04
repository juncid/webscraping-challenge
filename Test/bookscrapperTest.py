import unittest
from bs4 import BeautifulSoup
import re


class BookScrapperTest(unittest.TestCase):

    def setUp(self):
        html_book = """<body id="default" class="default">




    <header class="header container-fluid">
        <div class="page_inner">
            <div class="row">
                <div class="col-sm-8 h1"><a href="../../index.html">Books to Scrape</a><small> We love being scraped!</small>
</div>


            </div>
        </div>
    </header>



        <div class="container-fluid page">
            <div class="page_inner">

<ul class="breadcrumb">
    <li>
        <a href="../../index.html">Home</a>
    </li>


        <li>
            <a href="../category/books_1/index.html">Books</a>
        </li>

        <li>
            <a href="../category/books/poetry_23/index.html">Poetry</a>
        </li>

        <li class="active">A Light in the Attic</li>




</ul>







<div id="messages">

</div>


                <div class="content">



                    <div id="promotions">

                    </div>


                    <div id="content_inner">

<article class="product_page"><!-- Start of product page -->

    <div class="row">


        <div class="col-sm-6">










        <div id="product_gallery" class="carousel">
            <div class="thumbnail">
                <div class="carousel-inner">
                    <div class="item active">


                            <img src="../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg" alt="A Light in the Attic">


                    </div>
                </div>
            </div>
        </div>




        </div>



        <div class="col-sm-6 product_main">













        <h1>A Light in the Attic</h1><p class="price_color">£51.77</p>


<p class="instock availability">
    <i class="icon-ok"></i>

        In stock (22 available)

</p>








    <p class="star-rating Three">
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>
        <i class="icon-star"></i>

        <!-- <small><a href="/catalogue/a-light-in-the-attic_1000/reviews/">


                    0 customer reviews

        </a></small>
         -->&nbsp;


<!-- 
    <a id="write_review" href="/catalogue/a-light-in-the-attic_1000/reviews/add/#addreview" class="btn btn-success btn-sm">
        Write a review
    </a>

 --></p>



            <hr>

            <div class="alert alert-warning" role="alert"><strong>Warning!</strong> This is a demo website for web scraping purposes. Prices and ratings here were randomly assigned and have no real meaning.</div>











        </div><!-- /col-sm-6 -->


    </div><!-- /row -->



        <div id="product_description" class="sub-header">
            <h2>Product Description</h2>
        </div>
        <p>It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love th It's hard to imagine a world without A Light in the Attic. This now-classic collection of poetry and drawings from Shel Silverstein celebrates its 20th anniversary with this special edition. Silverstein's humorous and creative verse can amuse the dowdiest of readers. Lemon-faced adults and fidgety kids sit still and read these rhythmic words and laugh and smile and love that Silverstein. Need proof of his genius? RockabyeRockabye baby, in the treetopDon't you know a treetopIs no safe place to rock?And who put you up there,And your cradle, too?Baby, I think someone down here'sGot it in for you. Shel, you never sounded so good. ...more</p>




    <div class="sub-header">
        <h2>Product Information</h2>
    </div>
    <table class="table table-striped">

        <tbody><tr>
            <th>UPC</th><td>a897fe39b1053632</td>
        </tr>

        <tr>
            <th>Product Type</th><td>Books</td>
        </tr>



            <tr>
                <th>Price (excl. tax)</th><td>£51.77</td>
            </tr>

                <tr>
                    <th>Price (incl. tax)</th><td>£51.77</td>
                </tr>
                <tr>
                    <th>Tax</th><td>£0.00</td>
                </tr>

            <tr>
                <th>Availability</th>
                <td>In stock (22 available)</td>
            </tr>



            <tr>
                <th>Number of reviews</th>
                <td>0</td>
            </tr>

    </tbody></table>




        <section>
            <div id="reviews" class="sub-header">
            </div>
        </section>















</article><!-- End of product page -->
</div>
                </div>
            </div>
        </div>



<footer class="footer container-fluid">



</footer>





            <!-- jQuery -->
            <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <script>window.jQuery || document.write('<script src="../../static/oscar/js/jquery/jquery-1.9.1.min.js"><\/script>')</script>








    <!-- Twitter Bootstrap -->
    <script type="text/javascript" src="../../static/oscar/js/bootstrap3/bootstrap.min.js"></script>
    <!-- Oscar -->
    <script src="../../static/oscar/js/oscar/ui.js" type="text/javascript" charset="utf-8"></script>

    <script src="../../static/oscar/js/bootstrap-datetimepicker/bootstrap-datetimepicker.js" type="text/javascript" charset="utf-8"></script>
    <script src="../../static/oscar/js/bootstrap-datetimepicker/locales/bootstrap-datetimepicker.all.js" type="text/javascript" charset="utf-8"></script>












        <script type="text/javascript">
            $(function() {


    oscar.init();

            });
        </script>


        <!-- Version: N/A -->



</body>
"""
        self.soup_book = BeautifulSoup(html_book, 'html.parser')
        html_upc = """<tr>
            <th>UPC</th><td>a897fe39b1053632</td>
        </tr>"""
        self.soup_upc = BeautifulSoup(html_upc, 'html.parser')
        html_product_type = """<tr>
            <th>Product Type</th><td>Books</td>
        </tr>"""
        self.soup_product_type = BeautifulSoup(html_product_type, 'html.parser')
        html_price_excl_tax = """<tr>
                <th>Price (excl. tax)</th><td>£51.77</td>
            </tr>"""
        self.soup_price_excl_tax = BeautifulSoup(html_price_excl_tax, 'html.parser')
        html_price_incl_tax = """<tr>
                    <th>Price (incl. tax)</th><td>£51.77</td>
                </tr>"""
        self.soup_price_incl_tax = BeautifulSoup(html_price_incl_tax, 'html.parser')
        html_tax = """<tr>
                    <th>Tax</th><td>£0.00</td>
                </tr>"""
        self.soup_tax = BeautifulSoup(html_tax, 'html.parser')
        html_number_review = """<tr>
                <th>Number of reviews</th>
                <td>0</td>
            </tr>"""
        self.soup_number_review = BeautifulSoup(html_number_review, 'html.parser')

    def test_getTitleBook(self):
        title = self.soup_book.find('div', class_=re.compile('product_main')).h1.text
        self.assertEqual(title, "A Light in the Attic")

    def test_getPriceBook(self):
        price = self.soup_book.find('p', class_='price_color').text[1:]
        self.assertEqual(price, "51.77")

    def test_getStockBook(self):
        stock = re.sub("[^0-9]", "", self.soup_book.find('p', class_='instock availability').text)
        self.assertEqual(stock, "22")

    def test_getCategoryBook(self):
        category = self.soup_book.find('a', href=re.compile('../category/books/')).get('href').split('/')[3]
        self.assertEqual(category, "poetry_23")

    def test_getCoverBook(self):
        cover = self.soup_book.find('img').get('src')
        self.assertEqual(cover, "../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg")

    def test_getReviewsBook(self):
        review = self.soup_book.find('p', class_="star-rating").get('class')[1]
        self.assertEqual(review, 'Three')

    def test_getUpcBook(self):
        upc = self.soup_upc.find('td').text
        self.assertEqual(upc, 'a897fe39b1053632')

    def test_getProductTypeBook(self):
        product_type = self.soup_product_type.find('td').text
        self.assertEqual(product_type, 'Books')

    def test_getPriceExclTaxBook(self):
        price_excl_tax = re.sub("[^0-9.]", "", self.soup_price_excl_tax.find('td').text)
        self.assertEqual(price_excl_tax, '51.77')

    def test_getPriceInclTaxBook(self):
        price_incl_tax = re.sub("[^0-9.]", "", self.soup_price_incl_tax.find('td').text)
        self.assertEqual(price_incl_tax, '51.77')

    def test_getTaxBook(self):
        tax = re.sub("[^0-9.]", "", self.soup_tax.find('td').text)
        self.assertEqual(tax, '0.00')

    def test_getNumberReviewsBook(self):
        number_reviews = re.sub("[^0-9.]", "", self.soup_number_review.find('td').text)
        self.assertEqual(number_reviews, '0')
