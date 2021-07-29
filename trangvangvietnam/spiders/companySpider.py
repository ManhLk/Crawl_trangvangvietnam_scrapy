import numpy as np
import scrapy
from scrapy.http.request import Request
from trangvangvietnam.items import CompanyItem
from datetime import datetime

class CompanySpider(scrapy.Spider):
    name = "trangvangvietnam"
    start_urls = ["https://trangvangvietnam.com/findex.asp"]

    def parse(self, response):
        final_page = int(response.xpath('//div[@id="paging"]//a/text()').extract()[-2]) + 1
        url = response.url
        for page in range(1, final_page):
            url_ = url + "?page={}".format(page)
            yield Request(url_, callback=self.get_group_company, dont_filter=True)
    
    def get_group_company(self, response):
        list_group_company = response.xpath('//div[@style="height:23px; width:588px; float:left"]//p[@style="font-size:15px"]//a[@style="color:#00C"]/@href').extract()
        for group_company in list_group_company:
            yield Request(group_company, callback=self.next_page, dont_filter=True)
    
    def next_page(self, response):
        final_page = int(response.xpath('//div[@id="paging"]/a/text()').extract()[-2]) + 1
        url = response.url
        for page in range(1, final_page):
            url_ = url + "?page={}".format(page)
            yield Request(url_, callback=self.get_list_company, dont_filter=True)

    def get_list_company(self, response):
        list_company = response.xpath('//div[@class="noidungchinh"]//h2[@class="company_name"]//a/@href').extract()
        for url_compnay in list_company:
            yield Request(url_compnay, callback=self.get_company, dont_filter=True)

    def get_company(self, response):
        item = CompanyItem()
        # Name
        try:
            item['name'] = response.xpath("//div[@class='thongtinchitiet']//div[@class='hosocongty_li']//div[@class='hosocongty_text']//text()").extract()[0]
            item['name'] = item['name'].strip()
        except:
            item['name'] = np.nan

        # Tax code
        try:
            detail = response.xpath("//div[@class='thongtinchitiet']//div[@class='hosocongty_li']//div[@class='hosocongty_text']//text()").extract()
            for d in detail:
                if str(d).isdigit() and len(str(d)) > 5:
                    item['tax_code'] = d
            if 'tax_code' not in item:
                item['tax_code'] = np.nan
        except:
            item['tax_code'] = np.nan

        # establish at 
        try:  
            item['established_at'] = np.nan
            detail = response.xpath("//div[@class='thongtinchitiet']//div[@class='hosocongty_li']//div[@class='hosocongty_text']//text()").extract()
            for d in detail:
                d = str(d)
                if d.isdigit() and (int(d) >= 1000 and int(d)<= datetime.today().year):
                    item['established_at'] = d
        except:
            item['established_at'] = np.nan

        # Introduce
        try:
            item['introduce'] = response.xpath('//div[@class="thongtinchitiet"]//div[@class="gioithieucongty"]//p//text()').extract()
        except:
            item['introduce'] = np.nan

        # Industry
        try:
            industry = response.xpath('//div[@class="nganhnghe_chitiet_li"]//div[@class="nganhgnhe_chitiet_text"]//p//a/text()').extract()
            industry = [info.strip() for info in industry]
            item["industry"] = industry
        except:
            item["industry"] = np.nan

        # Product
        try:
            if len(response.xpath('//div[@class="sp_khongphannhom_box"]//div[@class="sp_khongphannhom_name"]//a/text()').extract()) > 0:
                # Lấy thông tin sản phẩm không phân nhóm
                item["product"] = response.xpath('//div[@class="sp_khongphannhom_box"]//div[@class="sp_khongphannhom_name"]//a/text()').extract()
            elif len(response.xpath('//div[@class="sanphamdichvu_phannhom_box"]')) > 0:
                # Lấy thông tin sản phẩm phân nhóm
                product = {}
                for group in response.xpath('//div[@class="sanphamdichvu_phannhom_box"]'):
                    group_product_name = group.xpath('.//div[@class="sanphamdichvu_tennhomsp"]//div[@class="tennhom_sp_text"]//p//span/text()').get()
                    product[group_product_name] = group.xpath('.//div[@class="sanphamdichvu_noidung"]//div[@class="tensanphamdichvu_box"]//div[@class="tensanphamdichvu_name"]//a/text()').extract()
                item["product"] = product
            else:
                item["product"] = np.nan
        except:
            item["product"] = np.nan

        # Website
        try:
            website = response.xpath('//div[@class="text_website"]//a/text()').get()
            item['website'] = website
        except:
            item['website'] = np.nan

        # Email
        try:
            email = response.xpath('//div[@class="text_email"]//p//a/text()').get()
            item['email'] = email
        except:
            item['email'] = np.nan    

        # Address
        try:
            item["address"] = response.xpath('//div[@class="diachi_chitietcongty"]//div[@class="diachi_chitiet_li"]//div[@class="diachi_chitiet_li2dc"]//p/text()').extract()
            item["address"] = [info.strip() for info in item["address"] if info.strip()!='']
            item["address"] = ''.join(item["address"])
        except:
            item["address"] = np.nan

        # phone number
        try:
            item["phone_number"] = response.xpath('//div[@class="diachi_chitietcongty"]//div[@class="diachi_chitiet_li"]//div[@class="diachi_chitiet_li2"]//span/text()').get()
            item["phone_number"] = item["phone_number"].replace(" ", '')
            item["phone_number"] = item["phone_number"].replace(",", '')
        except:
            item["phone_number"] = np.nan

        # fax
        try:
            item["fax"] = response.xpath('//div[@class="diachi_chitietcongty"]//div[@class="diachi_chitiet_li"]//div[@class="diachi_chitiet_li2"]//p/text()').get()
            item["fax"] = item["fax"].replace(" ", '')
            item["fax"] = item["fax"].replace(",", '')
        except:
            item["fax"] = np.nan

        # Create at:
        try:
            item["created_at"] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        except:
            item["created_at"] = np.nan

        return item
