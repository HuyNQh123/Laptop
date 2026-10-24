from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Laptop(db.Model):
    __tablename__ = 'laptops'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(50), nullable=False, index=True)
    cpu = db.Column(db.String(150), nullable=False)
    cpu_score = db.Column(db.Integer, nullable=False, default=0)
    gpu = db.Column(db.String(150), nullable=False)
    gpu_score = db.Column(db.Integer, nullable=False, default=0)
    ram = db.Column(db.Integer, nullable=False, default=8)
    storage = db.Column(db.Integer, nullable=False, default=512)
    screen_size = db.Column(db.Float, nullable=False, default=14.0)
    resolution = db.Column(db.String(50), default='1920x1080')
    refresh_rate = db.Column(db.Integer, default=60)
    weight = db.Column(db.Float, default=1.5)
    battery = db.Column(db.Float, default=50.0)
    operating_system = db.Column(db.String(100), default='Windows 11 Home')
    rating = db.Column(db.Float, default=4.5)
    price = db.Column(db.Float, nullable=False, default=0.0)
    units_sold = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'cpu': self.cpu,
            'cpu_score': self.cpu_score,
            'gpu': self.gpu,
            'gpu_score': self.gpu_score,
            'ram': self.ram,
            'storage': self.storage,
            'screen_size': self.screen_size,
            'resolution': self.resolution,
            'refresh_rate': self.refresh_rate,
            'weight': self.weight,
            'battery': self.battery,
            'operating_system': self.operating_system,
            'rating': self.rating,
            'price': self.price,
            'units_sold': self.units_sold
        }

    def __repr__(self):
        return f"<Laptop id={self.id} name='{self.name}' price={self.price}>"


class LaptopSource(db.Model):
    __tablename__ = 'laptop_sources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    laptop_name = db.Column(db.String(255), nullable=False, index=True)
    field_name = db.Column(db.String(255))
    source_name = db.Column(db.String(255))
    source_url = db.Column(db.Text)
    verified_date = db.Column(db.String(50))
    status = db.Column(db.String(50))
    note = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'laptop_name': self.laptop_name,
            'field_name': self.field_name,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'verified_date': self.verified_date,
            'status': self.status,
            'note': self.note
        }
