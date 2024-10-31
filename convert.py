import csv
import re
from datetime import datetime

CABECERA_RSS = """
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>Documentos RNE</title>
    <link>https://www.rtve.es/play/audios/documentos-rne/</link>
    <description>&apos;Documentos RNE&apos;, tras sus dos décadas de historia, ha logrado convertirse en un referente de los espacios documentales en la radiodifusión española.</description>
    <language>es</language>
    <itunes:owner>
      <itunes:email>movil.irtve@rtve.es</itunes:email>
      <itunes:name>RTVE</itunes:name>
    </itunes:owner>
    <itunes:image href="https://img2.rtve.es/imagenes/documentos-rne/1663661964535.jpg"></itunes:image>
    <itunes:category text="Society &amp; Culture"></itunes:category>
    <itunes:author>Radio Nacional</itunes:author>
    <itunes:explicit>no</itunes:explicit>
    <itunes:keywords></itunes:keywords>
    <itunes:summary>&apos;Documentos RNE&apos;, tras sus dos décadas de historia, ha logrado convertirse en un referente de los espacios documentales en la radiodifusión española.</itunes:summary>
    <image>
      <title>Documentos RNE</title>
      <url>https://img2.rtve.es/imagenes/documentos-rne/1663661964535.jpg</url>
      <link>https://www.rtve.es/play/audios/documentos-rne/</link>
    </image>
"""
ITEM_RSS = """
    <item>
      <title>{title}</title>
      <description>{title}</description>
      <enclosure url="{mp3}" type="audio/mpeg"></enclosure>
      <category>Radio/Programas de RNE/Documentales/Documentos RNE</category>
      <pubDate>{pubdate}</pubDate>
      <guid>https://www.rtve.es/a/{id}/</guid>
      <itunes:explicit>no</itunes:explicit>
      <itunes:keywords>Radio, Programas de RNE, Documentales, Documentos RNE</itunes:keywords>
      <itunes:image href="{img}"></itunes:image>
    </item>
"""
COLA_RSS = """
  </channel>
</rss>
"""

info = {}
patron = re.compile(r"-i (\d+).mp3 -i (\d+).jpg .* '(\d{4})-(\d{2})-(\d{2})")
with open('data/summary_documentosRNE.txt', encoding='utf-8') as f:
    for lin in f.readlines():
        m = patron.search(lin)
        if m is not None:
            info[m.groups()[0]] = m.groups()
with open('rss.xml', 'w', encoding='utf-8') as salida:
    salida.write(CABECERA_RSS)
    with open('README.md', encoding='utf-8') as entrada:
        for i in range(12):
            next(entrada)
        reader = csv.DictReader(entrada, delimiter='|', quoting=csv.QUOTE_NONE, skipinitialspace=True)
        for lin in reader:
            id = lin['id '].strip()
            title = lin['title                                                                       '].strip().replace('&nbsp;', ' ')
            mp3 = lin['mp3                                    '].strip()
            date = lin['date '].strip()
            if id.isdigit():
                if id in info:
                    _, imagen, ano, mes, dia = info[id]
                else:
                    imagen = None
                    ano = date
                    mes = 1
                    dia = 1
                fecha = datetime(int(ano), int(mes), int(dia)).strftime("%a, %d %b %Y %H:%M:%S GMT")
                img = f"https://img2.rtve.es/a/{imagen}/square/?h=320" if imagen is not None else "https://img2.rtve.es/p/1938/imgbackground/?h=320"
                salida.write(ITEM_RSS.format(
                    title=title,
                    mp3=mp3,
                    pubdate=fecha,
                    id=id,
                    img=img
                ))
    salida.write(COLA_RSS)

