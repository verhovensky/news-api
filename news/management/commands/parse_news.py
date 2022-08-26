from django.core.management.base import BaseCommand
from news.serializers import PostREADSerializer
from django.utils.text import slugify
from datetime import datetime
from .yoparser import parse_news_links_ozon, parse_news_links_yandex, \
    parse_single_article_link_yandex, parse_single_article_link_ozon


class Command(BaseCommand):
    help = "Parse news from Yandex and Ozon"

    def handle(self, *args, **options):
        # TODO: try except (KeyError)
        self.stdout.write(self.style.SUCCESS("Start parsing..."))
        ozon = parse_news_links_ozon()
        for i in ozon.items():
            b = parse_single_article_link_ozon(i[1]["link"])
            date = datetime.strptime(i[1]["date"].strip("Z"),
                                     "%Y-%m-%dT%H:%M:%S.%f")
            serializer = PostREADSerializer(
                data={"title": i[1]["title"],
                      "body": b["body"],
                      "date": date,
                      "slug": i[1]["slug"],
                      "tags": i[1]["tags"]})
            if serializer.is_valid():
                serializer.save()
            else:
                self.stdout.write(f"Data not valid: "
                                  f"{serializer.errors}")
        self.stdout.write(self.style.SUCCESS(
            f"Parsed and loaded {len(ozon)} Ozon news"))
        yandex = parse_news_links_yandex()
        for i in yandex.items():
            b = parse_single_article_link_yandex(i[1])
            date = datetime.strptime(b["date"].strip('+03:00'),
                                     "%Y-%m-%dT%H:%M:%S")
            slug = slugify(b["title"], allow_unicode=True)
            serializer = PostREADSerializer(
                data={"title": b["title"],
                      "body": b["body"],
                      "date": date,
                      "slug": slug,
                      "tags": b["tags"]})
            if serializer.is_valid():
                serializer.save()
            else:
                self.stdout.write(
                    f"Data not valid: {serializer.errors}")
        self.stdout.write(self.style.SUCCESS(f"Parsed and loaded "
                                             f"{len(yandex)} Yandex news"))
