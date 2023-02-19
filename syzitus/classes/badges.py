from flask import render_template
import time
from sqlalchemy import Column, Integer, String, ForeignKey

from syzitus.__main__ import Base, app


class BadgeDef():

    id = Column(Integer, primary_key=True)


    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):

        return f"<BadgeDef(badge_id={self.id})>"

    @property
    def path(self):

        return f"/assets/images/badges/{self.icon}"

    @property
    def json_core(self):
        data={
            "name": self.name,
            "description": self.description,
            "icon": self.icon
        }

    def evaluate(self, user):

        expr=self.__dict__.get("expr")

        if not expr:
            return None

        return bool(expr(user))
    


class Badge(Base):

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'))
    badge_id = Column(Integer)
    description = Column(String(64))
    url = Column(String(256))
    created_utc = Column(Integer)

    def __init__(self, *args, **kwargs):

        if "created_utc" not in kwargs:
            kwargs["created_utc"] = int(time.time())

        super().__init__(*args, **kwargs)

    def __repr__(self):

        return f"<Badge(user_id={self.user_id}, badge_id={self.badge_id})>"

    @property
    def badge(self):
        return BADGE_DEFS[self.badge_id]

    @property
    def text(self):
        if self.description:
            return self.description
        else:
            return self.badge.description

    @property
    def type(self):
        return self.badge.id

    @property
    def name(self):
        return self.badge.name

    @property
    def path(self):
        return self.badge.path

    @property
    def rendered(self):

        return render_template("badge.html", b=self)

    @property
    def json_core(self):

        return {'text': self.text,
                'name': self.name,
                'created_utc': self.created_utc,
                'url': self.url,
                'icon_url':f"https://{app.config['SERVER_NAME']}{self.path}"
                }

    property
    def json(self):
        return self.json_core

KINDS={
    1: "regular",
    2: "awarded",
    3: "discontinued",
    4: "special"
}

BADGE_DATA={
    1: {
        "name":"Artist",
        "description":f"Contributed art or other graphics to {app.config['SITE_NAME']}",
        "kind": 2,
        "rank": 3,
        "icon": "art.png"
    },
    2: {
        "name":"New User",
        "description":f"Joined {app.config['SITE_NAME']} within the last 30 days",
        "kind": 1,
        "rank": 1,
        "icon": "baby.png",
        "expr": lambda x: x.age<60*60*24*30
    },
    3: {
        "name":"Code Contributor",
        "description":f"Contributed code to {app.config['SITE_NAME']}",
        "kind": 2,
        "rank": 3,
        "icon": "git.png"
    },
    4: {
        "name":"Idea",
        "description":f"Provided a good idea for {app.config['SITE_NAME']} that was eventually added",
        "kind": 2,
        "rank": 2,
        "icon": "idea.png"
    },
    5: {
        "name":"Lab Rat",
        "description":"Helped test out new or experimental features",
        "kind": 2,
        "rank": 3,
        "icon": "labrat.png"
    },
    6: {
        "name":"Verified Email",
        "description":"Verified an email address",
        "kind": 1,
        "rank": 1,
        "icon": "mail.png",
        "expr": lambda x: x.is_activated
    },
    7: {
        "name":"Recruiter I",
        "description":f"Referred a friend to join {app.config['SITE_NAME']}",
        "kind": 1,
        "rank": 1,
        "icon": "recruit-1.png",
        "expr": lambda x: x.referral_count and x.referral_count >=1 and x.referral_count <10
    },
    8: {
        "name":"Recruiter II",
        "description":f"Referred 10 friends to join {app.config['SITE_NAME']}",
        "kind": 1,
        "rank": 1,
        "icon": "recruit-10.png",
        "expr": lambda x: x.referral_count and x.referral_count >=10 and x.referral_count <100
    },
    9: {
        "name":"Recruiter III",
        "description":f"Referred 100 friends to join {app.config['SITE_NAME']}",
        "kind": 1,
        "rank": 1,
        "icon": "recruit-100.png",
        "expr": lambda x: x.referral_count and x.referral_count >=100 and x.referral_count <1000
    },
    10: {
        "name":"Recruiter IV",
        "description":f"Referred 1000 friends to join {app.config['SITE_NAME']}",
        "kind": 1,
        "rank": 1,
        "icon": "recruit-1000.png",
        "expr": lambda x: x.referral_count and x.referral_count >=100
    },
    11: {
        "name":"Sitebreaker",
        "description":f"Involuntarily QA tested {app.config['SITE_NAME']}.",
        "kind": 2,
        "rank": 2,
        "icon": "sitebreaker.png"
    },
    12: {
        "name":"White Hat Hacker",
        "description":f"Responsibly disclosed a security vulnerability to {app.config['SITE_NAME']} staff.",
        "kind": 2,
        "rank": 3,
        "icon": "whitehat.png"
    },
    13: {
        "name":"1 Year",
        "description":"Joined a year ago.",
        "kind": 1,
        "rank": 5,
        "icon": "year-1.png",
        "expr": lambda x: x.age_string=="1 year ago"
    },
    14: {
        "name":"2 Year",
        "description":"Joined two years ago.",
        "kind": 1,
        "rank": 5,
        "icon": "year-2.png",
        "expr": lambda x: x.age_string=="2 years ago"
    },
    15: {
        "name":"Alpha User",
        "description":f"Joined {app.config['SITE_NAME']} in alpha phase",
        "kind": 3,
        "rank": 4,
        "icon": "alpha.png"
    },
    16: {
        "name":"Beta User",
        "description":f"Joined {app.config['SITE_NAME']} in beta phase",
        "kind": 3,
        "rank": 3,
        "icon": "beta.png"
    },
    17: {
        "name":"Halloween Runners-Up 2022",
        "description":f"Fought in vain to free Halloween from Christmas tyranny in the 2022 Holiday War",
        "kind": 5,
        "rank": 3,
        "icon": "holiday-2022-hween.png"
    },
    18: {
        "name":"Christmas Victors 2022",
        "description":f"Successfully defended Christmas from the Halloween invasion in the 2022 Holiday War",
        "kind": 5,
        "rank": 2,
        "icon": "holiday-2022-xmas.png"
    }
}

BADGE_DEFS={x:BadgeDef(id=x, **BADGE_DATA[x]) for x in BADGE_DATA}


