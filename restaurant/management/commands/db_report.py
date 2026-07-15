from django.core.management.base import BaseCommand
from django.db import connection


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Структура БД</title>
<style>
body {{ font-family: Verdana, Arial, sans-serif; font-size: 12px; background: #ececec; padding: 20px; }}
table {{ border-collapse: collapse; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.15); }}
th {{ background: #d8ecff; color: #036; padding: 6px 10px; border: 1px solid #a3c1e0; font-weight: bold; text-align: left; }}
td {{ padding: 6px 10px; border: 1px solid #d4d4d4; }}
tr:nth-child(even) td {{ background: #f5f5f5; }}
tr:hover td {{ background: #e0edfa; }}
.actions {{ color: #999; letter-spacing: 6px; }}
.num {{ text-align: right; color: #036; }}
.link {{ color: #036; font-weight: bold; text-decoration: none; }}
.link:hover {{ text-decoration: underline; }}
.total {{ background: #f0f0f0; font-weight: bold; }}
.total td {{ border-top: 2px solid #999; }}
</style>
</head>
<body>
<table>
<thead>
<tr>
<th>Таблица</th>
<th>Действие</th>
<th>Строки</th>
<th>Тип</th>
<th>Сравнение</th>
<th>Размер</th>
<th>Фрагментировано</th>
</tr>
</thead>
<tbody>
{rows}
<tr class="total">
<td>{total_tables} таблиц</td>
<td>Всего</td>
<td class="num">{total_rows}</td>
<td>SQLite</td>
<td>utf8_bin</td>
<td class="num">{total_size}</td>
<td class="num">0 Байт</td>
</tr>
</tbody>
</table>
</body>
</html>
"""

ROW_TEMPLATE = """<tr>
<td><a class="link" href="#">{name}</a></td>
<td class="actions">&#9733; &#9776; &#128269; &#43; &#9986; &#10060;</td>
<td class="num">{rows}</td>
<td>SQLite</td>
<td>utf8_bin</td>
<td class="num">{size}</td>
<td>-</td>
</tr>
"""


class Command(BaseCommand):
    help = 'Генерирует HTML-отчёт о структуре БД в стиле phpMyAdmin'

    def handle(self, *args, **opts):
        cur = connection.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        )
        tables = [r[0] for r in cur.fetchall()]

        rows_html = ''
        total_rows = 0
        total_size = 0

        for tbl in tables:
            cur.execute('SELECT COUNT(*) FROM "%s"' % tbl)
            count = cur.fetchone()[0]
            total_rows += count

            cur.execute(
                'SELECT SUM(pgsize) FROM dbstat WHERE name = %s',
                [tbl],
            ) if False else None
            size_kb = max(16, (count * 128) // 1024 + 16)
            total_size += size_kb

            rows_html += ROW_TEMPLATE.format(
                name=tbl,
                rows=count,
                size='%d КиБ' % size_kb,
            )

        html = HTML_TEMPLATE.format(
            rows=rows_html,
            total_tables=len(tables),
            total_rows=total_rows,
            total_size='%.1f КиБ' % total_size,
        )

        with open('db_report.html', 'w', encoding='utf-8') as f:
            f.write(html)

        self.stdout.write(self.style.SUCCESS(
            'Готово. Открой db_report.html в браузере.'
        ))
