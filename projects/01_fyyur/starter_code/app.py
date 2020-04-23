#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database +

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    past_shows = db.Column(db.ARRAY(db.Integer), nullable=False, default=[])
    upcoming_shows = db.Column(
        db.ARRAY(db.Integer), nullable=False, default=[])
    past_shows_count = db.Column(db.Integer, nullable=False, default=0)
    upcoming_shows_count = db.Column(db.Integer, nullable=False, default=0)
    db.relationship('Show', backref='venue', cascade='all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate+


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    past_shows = db.Column(db.ARRAY(db.Integer), nullable=False, default=[])
    upcoming_shows = db.Column(
        db.ARRAY(db.Integer), nullable=False, default=[])
    past_shows_count = db.Column(db.Integer, nullable=False, default=0)
    upcoming_shows_count = db.Column(db.Integer, nullable=False, default=0)
    db.relationship('Show', backref='artist', cascade='all, delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate+


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(100), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.+

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.+
    venues = Venue.query.order_by('city').all()

    data = []
    objects_count = 0
    for venue in venues:
        if objects_count == 0 or not data[objects_count-1]['city'] == venue.city:
            objects_count += 1
            data.append({
                "city": venue.city,
                "state": venue.state,
                "venues": [{
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": venue.upcoming_shows_count
                }]
            })
        else:
            data[objects_count-1]['venues'].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.upcoming_shows_count
            })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.+
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    venues = Venue.query.all()
    search_term = request.form.get('search_term', '').lower()
    count = 0
    data = []
    for venue in venues:
        if search_term in venue.name.lower():
            count += 1
            data.append({
                'id': venue.id,
                "name": venue.name,
                "num_upcoming_shows": venue.upcoming_shows_count
            })
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id+
    venue = Venue.query.get(venue_id)
    past_shows = []
    for shows in venue.past_shows:
        show = Show.query.get(shows)
        past_show = {
            "artist_id": show.artist_id,
            "artist_name": Artist.query.get(show.artist_id).name,
            "artist_image_link": Artist.query.get(show.artist_id).image_link,
            "start_time": show.start_time
        }
        past_shows.append(past_show)
    upcoming_shows = []
    for shows in venue.upcoming_shows:
        show = Show.query.get(shows)
        upcoming_show = {
            "artist_id": show.artist_id,
            "artist_name": Artist.query.get(show.artist_id).name,
            "artist_image_link": Artist.query.get(show.artist_id).image_link,
            "start_time": show.start_time
        }
        upcoming_shows.append(upcoming_show)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": venue.past_shows_count,
        "upcoming_shows_count": venue.upcoming_shows_count,
    }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead+
    # TODO: modify data to be the data object returned from db insertion+
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        if request.form['image_link'] == '':
            image_link = 'No Image Link'
        else:
            image_link = request.form['image_link']
        if request.form['website_link'] == '':
            website = 'No Website'
        else:
            website = request.form['website_link']
        if request.form['facebook_link'] == '':
            facebook_link = 'No Facebook Link'
        else:
            facebook_link = request.form['facebook_link']
        seeking_talent = request.form['seeking_talent']
        if seeking_talent == "True":
            seeking_talent = True
        else:
            seeking_talent = False
        if seeking_talent == True and request.form['seeking_description'] == '':
            seeking_description = 'Currently seeking performance venues'
        elif not seeking_talent == True and request.form['seeking_description'] == '':
            seeking_description = 'Not currently seeking performance venues'
        else:
            seeking_description = request.form['seeking_description']
        venue = Venue(name=name, city=city, state=state, phone=phone, address=address, image_link=image_link, genres=genres, website=website,
                      facebook_link=facebook_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except Exception as error:
        print("Oops! An exception has occured:", error)
        print("Exception TYPE:", type(error))
        error = True
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    # TODO: on unsuccessful db insert, flash an error instead.+
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.+
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database+
    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.+
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    artists = Artist.query.all()
    search_term = request.form.get('search_term', '').lower()
    count = 0
    data = []
    for artist in artists:
        if search_term in artist.name.lower():
            count += 1
            data.append({
                'id': artist.id,
                "name": artist.name,
                "num_upcoming_shows": artist.upcoming_shows_count
            })
    response = {
        "count": count,
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)
    venue = Venue.query.get(1)
    past_shows = []
    for shows in artist.past_shows:
        show = Show.query.get(shows)
        past_show = {
            "venue_id": show.artist_id,
            "venue_name": Venue.query.get(show.venue_id).name,
            "venue_image_link": Venue.query.get(show.venue_id).image_link,
            "start_time": show.start_time
        }
        past_shows.append(past_show)
    upcoming_shows = []
    for shows in artist.upcoming_shows:
        show = Show.query.get(shows)
        upcoming_show = {
            "venue_id": show.venue_id,
            "venue_name": Venue.query.get(show.venue_id).name,
            "venue_image_link": Venue.query.get(show.venue_id).image_link,
            "start_time": show.start_time
        }
        upcoming_shows.append(upcoming_show)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": artist.past_shows_count,
        "upcoming_shows_count": artist.upcoming_shows_count,
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    try:
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        if request.form['image_link'] == '':
            artist.image_link = 'No Image Link'
        else:
            artist.image_link = request.form['image_link']
        artist.genres = request.form.getlist('genres')
        if request.form['website_link'] == '':
            artist.website_link = 'No Website'
        else:
            artist.website_link = request.form['website_link']
        if request.form['facebook_link'] == '':
            artist.facebook_link = 'No Facebook Link'
        else:
            artist.facebook_link = request.form['facebook_link']
        seeking_venue = request.form['seeking_venue']
        if seeking_venue == "True":
            seeking_venue = True
        elif seeking_venue == "False":
            seeking_venue = False
        artist.seeking_venue = seeking_venue
        if artist.seeking_venue == True and request.form['seeking_description'] == '':
            artist.seeking_description = 'Currently seeking performance venues'
        elif not artist.seeking_venue == True and request.form['seeking_description'] == '':
            artist.seeking_description = 'Not currently seeking performance venues'
        else:
            artist.seeking_description = request.form['seeking_description']
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        error = True
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    venue = Venue.query.get(venue_id)
    try:
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = request.form.getlist('genres')
        if request.form['image_link'] == '':
            venue.image_link = 'No Image Link'
        else:
            venue.image_link = request.form['image_link']
        if request.form['website_link'] == '':
            venue.website = 'No Website'
        else:
            venue.website = request.form['website_link']
        if request.form['facebook_link'] == '':
            venue.facebook_link = 'No Facebook Link'
        else:
            venue.facebook_link = request.form['facebook_link']
        seeking_talent = request.form['seeking_talent']
        if seeking_talent == "True":
            seeking_talent = True
        elif seeking_talent == "False":
            seeking_talent = False
        venue.seeking_talent = seeking_talent
        if venue.seeking_talent == True and request.form['seeking_description'] == '':
            venue.seeking_description = 'Currently seeking performance venues'
        elif not venue.seeking_talent == True and request.form['seeking_description'] == '':
            venue.seeking_description = 'Not currently seeking performance venues'
        else:
            venue.seeking_description = request.form['seeking_description']
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as error:
        print("Oops! An exception has occured:", error)
        print("Exception TYPE:", type(error))
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        if request.form['image_link'] == '':
            image_link = 'No Image Link'
        else:
            image_link = request.form['image_link']
        genres = request.form.getlist('genres')
        if request.form['website_link'] == '':
            website_link = 'No Website'
        else:
            website_link = request.form['website_link']
        if request.form['facebook_link'] == '':
            facebook_link = 'No Facebook Link'
        else:
            facebook_link = request.form['facebook_link']
        seeking_venue = request.form['seeking_venue']
        if seeking_venue == "True":
            seeking_venue = True
        else:
            seeking_venue = False
        if seeking_venue == True and request.form['seeking_description'] == '':
            seeking_description = 'Currently seeking performance venues'
        elif not seeking_venue == True and request.form['seeking_description'] == '':
            seeking_description = 'Not currently seeking performance venues'
        else:
            seeking_description = request.form['seeking_description']
        artist = Artist(name=name, city=city, state=state, phone=phone, image_link=image_link, genres=genres, website_link=website_link,
                        facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        error = True
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    # on successful db insert, flash success+

    # TODO: on unsuccessful db insert, flash an error instead.+
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.+
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.get(show.venue_id).name,
            "artist_id": show.artist_id,
            "artist_name": Artist.query.get(show.artist_id).name,
            "artist_image_link": Artist.query.get(show.artist_id).image_link,
            "start_time": show.start_time
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead+
    new_show_date = 0
    current_date = format_datetime(babel.dates.format_datetime(format='short',
                                                               tzinfo=babel.dates.get_timezone('America/Denver')))
    current_day = current_date[8:10]
    current_month = current_date[4:6]
    current_year = current_date[14:16]
    current_date_total = current_year+current_month+current_day
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        year = start_time[2:4]
        month = start_time[5:7]
        day = start_time[8:10]
        new_show_date = year+month+day

    # on successful db insert, flash success
        show = Show(venue_id=venue_id, artist_id=artist_id,
                    start_time=start_time)
        db.session.add(show)
        db.session.commit()
        # if date is in the future or today, add show to future shows, else add to past shows
        if new_show_date >= current_date_total:
            venue_upcoming_shows = Venue.query.get(venue_id)
            artist_upcoming_shows = Artist.query.get(artist_id)
            venue_upcoming_shows.upcoming_shows = list(
                venue_upcoming_shows.upcoming_shows)
            venue_upcoming_shows.upcoming_shows.append(show.id)
            artist_upcoming_shows.upcoming_shows = list(
                artist_upcoming_shows.upcoming_shows)
            artist_upcoming_shows.upcoming_shows.append(
                show.id)
            venue_upcoming_shows.upcoming_shows_count += 1
            artist_upcoming_shows.upcoming_shows_count += 1
            db.session.commit()
        else:
            venue_past_shows = Venue.query.get(venue_id)
            artist_past_shows = Artist.query.get(artist_id)
            venue_past_shows.past_shows = list(venue_past_shows.past_shows)
            venue_past_shows.past_shows.append(
                show.id)
            artist_past_shows.past_shows = list(artist_past_shows.past_shows)
            artist_past_shows.past_shows.append(
                show.id)
            venue_past_shows.past_shows_count += 1
            artist_past_shows.past_shows_count += 1
            db.session.commit()
        flash('Show was successfully listed!')
    except Exception as error:
        print("Oops! An exception has occured:", error)
        print("Exception TYPE:", type(error))
        error = True
        # db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
