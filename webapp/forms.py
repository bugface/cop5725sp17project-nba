from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.
class CollegeForm(FlaskForm):
    coll = SelectField("College")
    sub1 = SubmitField("search")

    def edit_coll(self, colls):
        self.coll.choices = colls

class categotyForm(FlaskForm):
    model = SelectField("model")
    sub2 = SubmitField("search")

    def edit_model(self, m):
        self.model.choices = m

class PlayerSearchForm(FlaskForm):
    player_name = TextField(u'', render_kw={"placeholder": "Player Name"}, validators = [DataRequired()])
    go = SubmitField('Go!')

class CoachYearForm(FlaskForm):
    seas = SelectField("Season")
    submit = SubmitField('Submit')

    def edit_season(self, years):
        #form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
        self.seas.choices = years

class PlayerYearForm(FlaskForm):
    year = SelectField("Season")
    sub = SubmitField('Submit')

    def edit_year(self, years):
        #form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
        self.year.choices = years

class InsertForm(FlaskForm):
    h_team = TextField(
        'Home Team', validators=[DataRequired(), Length(min=0, max=50)]
        )
    a_team = TextField(
        'Away Team', validators=[DataRequired(), Length(min=0, max=50)]
        )
    date = DateField(
        'date', validators=[DataRequired()]
        )
    home_team_player = TextField(
        'Home player and data (player_name(pts, dreb, oreb, ast, );nextplayer'
        )
    away_team_player = TextField(
        'Away player and data (player_name(data1,data2...datak);nextplayer'
        )

    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(FlaskForm):
    name = TextField('Admin', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Submit')


class ForgotForm(FlaskForm):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
