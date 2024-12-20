import csv
from datetime import datetime
from models import db, Artist, Album, Song
from app import app


def import_data(file_path):
    with app.app_context():
        db.create_all()

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # 插入 Artist
                artist_name = row['artist_name']
                artist = Artist.query.filter_by(Name=artist_name).first()
                if not artist:
                    artist = Artist(Name=artist_name, Country='Unknown')  # 缺少国家信息时设为 Unknown
                    db.session.add(artist)
                    db.session.flush()  # 提交以获取 ArtistID

                # 插入 Album
                album_title = f"Album of {artist_name}"
                release_date = row.get('release_date', None)

                # 将 release_date 转换为 Python 的 date 对象
                if release_date and release_date.isdigit():
                    release_date = datetime.strptime(release_date, "%Y").date()
                elif release_date:  # 如果是完整的日期格式（例如 YYYY-MM-DD）
                    release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
                else:
                    release_date = None  # 没有 release_date 时设为 None

                album = Album.query.filter_by(Title=album_title, ArtistID=artist.ArtistID).first()
                if not album:
                    album = Album(Title=album_title, ArtistID=artist.ArtistID, ReleaseDate=release_date)
                    db.session.add(album)
                    db.session.flush()

                # 插入 Song
                song = Song(
                    Title=row['track_name'],
                    ArtistID=artist.ArtistID,
                    AlbumID=album.AlbumID,
                    Genre=row.get('genre', 'Unknown'),
                    Duration=row.get('len', 'Unknown'),
                    ReleaseDate=release_date
                )
                db.session.add(song)
            db.session.commit()


if __name__ == '__main__':
    import_data('data/song_dataset.csv')


