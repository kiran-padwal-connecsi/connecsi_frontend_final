import datetime
from functools import wraps
import json
import time

import requests
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging,jsonify
# from model.ConnecsiModel import ConnecsiModel
# from passlib.hash import sha256_crypt
#from flask_oauthlib.client import OAuth
import os
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
# from flask_paginate import Pagination, get_page_parameter
from flask_uploads import UploadSet, configure_uploads, IMAGES

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
# os.environ['WERKZEUG_RUN_MAIN'] = 'true'




connecsiApp = Flask(__name__)
connecsiApp.secret_key = 'connecsiSecretKey'
base_url = 'https://kiranpadwaltestconnecsi.pythonanywhere.com/api/'


google_blueprint = make_google_blueprint(
    client_id="413672402805-dvv0v7bft07iqhj2du2eqq59itbeqcv1.apps.googleusercontent.com",
    client_secret="wNxRXqxGrz7inj2yE2nlgcyO",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
    redirect_to='google_login'

)
twitter_blueprint = make_twitter_blueprint(
    api_key="lOhkeJRZhYXvkm0lYq1ZgTtYa",
    api_secret="TbMKSZBbcqhnedjjqG66JuStxunBdKLelfjgxTW4UNJndbatJa",
    redirect_to='twitter_login'
)
connecsiApp.register_blueprint(google_blueprint, url_prefix="/login")
connecsiApp.register_blueprint(twitter_blueprint, url_prefix="/login")

photos = UploadSet('photos', IMAGES)
connecsiApp.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(connecsiApp, photos)

@connecsiApp.route("/google_login")
def google_login():
    if not google.authorized:
        print('i m here always')
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    print(resp.json())
    resp_json = resp.json()
    # assert resp.ok, resp.text
    if resp.ok:
        user_id = resp_json['id']
        print(user_id)
        # exit()
        if user_id:
            flash("logged in", 'success')
            session['logged_in'] = True
            session['email_id'] = resp_json['email']
            session['type'] = 'influencer'
            session['user_id'] = user_id
            print(session['user_id'])
            return redirect(url_for('admin'))
    else:return redirect(url_for('login'))

@connecsiApp.route("/twitter_login")
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/verify_credentials.json?include_email=true")

    print(resp.json())
    # exit()
    resp_json = resp.json()
    # screen_name = resp_json['screen_name']
    # user_data = twitter.get('users/show.json?screen_name=' +screen_name)
    # assert resp.ok, resp.text
    # print(user_data.json())
    if resp.ok:
        user_id = resp_json['id']
        print(user_id)
        # exit()
        if user_id:
            flash("logged in", 'success')
            session['logged_in'] = True
            session['email_id'] = resp_json['email']
            session['type'] = 'influencer'
            session['user_id'] = user_id
            # print(session['user_id'])
            return redirect(url_for('admin'))
    else:return redirect(url_for('login'))





# oauth = OAuth(connecsiApp)

# linkedin = oauth.remote_app(
#     'linkedin',
#     consumer_key='86ctp4ayian53w',
#     consumer_secret='3fdovLJRbWrQuu3u',
#     request_token_params={
#         'scope': 'r_basicprofile,r_emailaddress',
#         'state': 'RandomString',
#     },
#     base_url='https://api.linkedin.com/v1/',
#     request_token_url=None,
#     access_token_method='POST',
#     access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
#     authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
# )

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for('index'))
    return wrap


@connecsiApp.route('/')
# @is_logged_in
def index():
    title='Connesi App Login Panel'
    data=[]
    data.append(title)
    return render_template('user/login.html',data=data)


@connecsiApp.route('/privacy_policy')
def privacy_policy():
    return render_template('user/privacy_policy.html')

# @connecsiApp.route('/loginLinkedin')
# def loginLinkedin():
#     return linkedin.authorize(callback=url_for('authorized', _external=True))

@connecsiApp.route('/registerBrand')
def registerBrand():
    return render_template('user/registerFormBrand.html')

@connecsiApp.route('/saveBrand',methods=['GET','POST'])
def saveBrand():
    if request.method == 'POST':
        url = base_url+'Brand/register'
        payload = request.form.to_dict()
        print(payload)
        del payload['confirm_password']
        print(payload)
        title = 'Connesi App Login Panel'
        try:
            response = requests.post(url, json=payload)
            print(response.json())
            result_json = response.json()
            print(result_json['response'])
            result = result_json['response']
            # exit()
            if result == 1:
                payload1 = {
                  "from_email_id": "business@connecsi.com",
                  "to_email_id": request.form.get('email'),
                  "date": datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                  "subject": "Welcome To Connecsi",
                  "message": "Hello User welcome to Connecsi"
                }
                user_id = 1
                type = 'brand'
                url = base_url + 'Messages/sentWelcomeEmail/' + str(user_id) + '/' + type
                try:
                    response = requests.post(url=url, json=payload1)
                    data = response.json()
                    print('email sent')
                except:
                    pass
                flash("Brand Details Successfully Registered", 'success')
                title = 'Connesi App Login Panel'
                return render_template('user/login.html', title=title)
            else:
                flash("Internal error please try later", 'danger')
                return render_template('user/login.html', title=title)
        except:
            flash("Internal error please try later", 'danger')
            return render_template('user/registerFormBrand.html',title='Register Brand')
#
#
#
#Logout
@connecsiApp.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('index'))

#
# # User login
@connecsiApp.route('/login',methods=['POST'])
def login():
    if request.method=='POST':
        if 'brand' in request.form:
            url = base_url + 'User/login'
            payload = request.form.to_dict()
            print(payload)
            del payload['brand']
            print(payload)
            title = ''
            try:
                response = requests.post(url, json=payload)
                print(response.json())
                result_json = response.json()
                user_id = result_json['user_id']
                print(user_id)
                # exit()
                if user_id:
                    flash("logged in", 'success')
                    session['logged_in'] = True
                    session['email_id']=payload.get('email')
                    session['type'] = 'brand'
                    session['user_id']=user_id
                    print(session['user_id'])
                    return redirect(url_for('admin'))
                else:
                    flash("Internal error please try later", 'danger')
                    return render_template('user/login.html', title=title)
            except:
                flash("Internal error please try later", 'danger')
                return render_template('user/login.html', title='Login')
        elif 'influencer' in request.form:
            email_id = request.form.get('inf_username')
            password = request.form.get('inf_password')
            print(email_id)
            print(password)

@connecsiApp.route('/admin')
@is_logged_in
def admin():
    title='Dashboard'
    return render_template('index.html',title=title)
#
#
@connecsiApp.route('/profileView')
@is_logged_in
def profileView():
    profileView.counter+=1
    if profileView.counter==1:
        title='Profile View'
        type = session['type']
        user_id = session['user_id']
        if type == 'brand':
            url = base_url + 'Brand/'+str(user_id)
            try:
                response = requests.get(url)
                # print(response.json())
                data_json = response.json()
                print(data_json)
                return render_template('user/user-profile-page.html', data=data_json, title=title)
            except Exception as e:
                print(e)
        else:
            table_name = 'users_inf'
    else:
        profileView.counter=0
        return ''
profileView.counter=0


@connecsiApp.route('/editProfile')
@is_logged_in
def editProfile():
    title='Edit Profile'
    type = session['type']
    user_id = session['user_id']
    if type == 'brand':
        url = base_url + 'Brand/'+str(user_id)
        try:
            response = requests.get(url)
            # print(response.json())
            data_json = response.json()
            print(data_json)
            return render_template('user/edit-profile-page.html', data=data_json, title=title)
        except Exception as e:
            print(e)
    else:
        table_name = 'users_inf'

@connecsiApp.route('/updateProfile',methods=['GET','POST'])
@is_logged_in
def updateProfile():
    user_id = session['user_id']
    if request.method == 'POST':
        url = base_url+ 'Brand/'+str(user_id)
        payload = request.form.to_dict()
        print(payload)
        try:
            response = requests.put(url=url,json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Successfully Updated Profile Data','success')
            return profileView()
        except:pass


@connecsiApp.route('/uploadProfilePic',methods=['GET','POST'])
@is_logged_in
def uploadProfilePic():
    user_id = session['user_id']
    if request.method == 'POST' and 'profile_pic' in request.files:
        filename = photos.save(request.files['profile_pic'])
        url = base_url + 'Brand/updateProfilePic/' + str(user_id)
        payload = {}
        payload.update({'profile_pic':filename})
        print(payload)
        try:
            response = requests.put(url=url, json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Successfully Updated Profile Pic', 'success')
            return editProfile()
        except:
            pass


@connecsiApp.route('/changePassword',methods=['POST'])
@is_logged_in
def changePassword():
    user_id=session['user_id']
    if request.method == 'POST':
        url = base_url+ 'Brand/changePassword/'+str(user_id)
        payload = request.form.to_dict()
        # print(payload)
        del payload['con_new_password']
        # print(payload)
        try:
            response = requests.put(url=url,json=payload)
            result_json = response.json()
            # return redirect(url_for('/profileView'))
            flash('Password Updated','success')
            return profileView()
        except:pass



@connecsiApp.route('/searchInfluencers',methods=['POST','GET'])
@is_logged_in
def searchInfluencers():
    searchInfluencers.counter+=1
    if searchInfluencers.counter==1:
        url_regionCodes = base_url + 'Youtube/regionCodes'
        regionCodes_json=''
        videoCat_json=''
        form_filters=''
        country_name=''
        view_campaign_data=''
        data=''
        favInfList_data=''
        try:
            response_regionCodes = requests.get(url=url_regionCodes)
            regionCodes_json = response_regionCodes.json()
            # print(regionCodes_json['data'])
        except Exception as e:
            print(e)
        url_videoCat = base_url + 'Youtube/videoCategories'
        try:
            response_videoCat = requests.get(url=url_videoCat)
            videoCat_json = response_videoCat.json()
            # print(videoCat_json['data'])
        except Exception as e:
            print(e)
        lookup_string = ''
        for cat in videoCat_json['data']:
            # print(cat['video_cat_name'])
            lookup_string += ''.join(',' + cat['video_cat_name'])
        lookup_string = lookup_string.replace('&', 'and')
        try:
            template, view_campaign_data = viewCampaigns()
        except Exception as e:
            print(e)
            pass

        try:
            template, favInfList_data = influencerFavoritesList()
        except Exception as e:
            print(e)
            pass
        # print('fav list = ',favInfList_data['data'])
        # for item in favInfList_data['data']:
        #     print(item['channel_id'])
        if request.method=='POST':
            if 'search_inf' in request.form:
                string_word = request.form.get('string_word')
                print('string word =',string_word)
                # exit()
                category = string_word.replace('and','&')
                print(category)
                category_id=''
                for cat in videoCat_json['data']:
                    # print(cat['video_cat_name'])
                    if cat['video_cat_name'] == category:
                        print("category id = ",cat['video_cat_id'])
                        category_id = cat['video_cat_id']
                form_filters = request.form.to_dict()
                print('post form filters =',form_filters)
                url_country_name = base_url + 'Youtube/regionCode/'+form_filters['country']
                try:
                    response_country_name = requests.get(url=url_country_name)
                    country_name_json = response_country_name.json()
                    print(country_name_json['data'][0][1])
                    country_name = country_name_json['data'][0][1]
                except Exception as e:
                    print(e)
                form_filters.update({'country_name':country_name})
                print('last filters = ',form_filters)
                payload = request.form.to_dict()

                del payload['string_word']
                del payload['search_inf']
                del payload['channel']
                payload.update({'category_id': str(category_id)})
                payload.update({'min_lower':payload.get('min_lower')})
                payload.update({'max_upper':payload.get('max_upper')})
                print(payload)

                try:
                    channel = request.form.get('channel')
                    url = base_url+'Youtube/searchChannels/'+channel
                    # print(url)
                    response = requests.post(url, json=payload)
                    # print(response.json())
                    data = response.json()
                    linechart_id=1
                    for item in data['data']:
                        item.update({'linechart_id':linechart_id})
                        print(item)
                        linechart_id+=1
                    # print(data)
                    # search = False
                    # q = request.args.get('page')
                    # if q:
                    #     search = True
                    # page = request.args.get(get_page_parameter(), type=int, default=1)
                    # pagination = Pagination(page=page, total=len(data['data']), search=search,
                    #                         record_name='Influencers',per_page=5)
                    # print(data)

                    # print(campaignsList)
                    return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                           lookup_string=lookup_string, form_filters=form_filters,data=data,view_campaign_data=view_campaign_data
                                           ,favInfList_data=favInfList_data)
                except Exception as e:
                    print(e)
                    print('i m hee')
                    return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                       lookup_string=lookup_string,form_filters=form_filters,data='',pagination='',view_campaign_data=view_campaign_data
                                           ,favInfList_data=favInfList_data)
        else:
            print('i m here last')
            try:
                payload = {
                    "category_id": "20",
                    "country": "PL",
                    "min_lower": 0,
                    "max_upper": 30000,
                    "sort_order": "High To Low"
                }
                url = base_url + 'Youtube/searchChannels/Youtube'
                response = requests.post(url, json=payload)
                print(response.json())
                data = response.json()
                linechart_id = 1
                for item in data['data']:
                    item.update({'linechart_id': linechart_id})
                    print(item)
                    linechart_id += 1
                form_filters = {'channel': 'Youtube', 'string_word': 'Gaming', 'country': 'PL', 'min_lower': '0', 'max_upper': '30000', 'search_inf': '', 'sort_order': 'High To Low', 'country_name': 'Poland'}
            except:
                pass
            return render_template('search/searchInfluencers.html', regionCodes=regionCodes_json,
                                   lookup_string=lookup_string,form_filters=form_filters,data=data,pagination='',view_campaign_data=view_campaign_data,
                                   favInfList_data=favInfList_data)
    else:
        searchInfluencers.counter=0
        return ''
searchInfluencers.counter=0


#
@connecsiApp.route('/addFundsBrands')
@is_logged_in
def addFundsBrands():
    return render_template('user/add_funds.html')


@connecsiApp.route('/saveFundsBrands',methods=['POST'])
@is_logged_in
def saveFundsBrands():
    if request.method == 'POST':
       payload = request.form.to_dict()
       print(payload)
       user_id = session['user_id']
       url = base_url+'Payments/'+str(user_id)
       try:
           response = requests.post(url=url, json=payload)
           result_json = response.json()
           flash('saved funds','success')
           return viewMyPayments()
       except:
           pass
    else:
        flash('No Funds added','danger')
        return redirect(url_for('addFundsBrands'))

#
# @connecsiApp.route('/payment')
# @is_logged_in
# def payment():
#     # print(user_id,date,email_id,amount,description)
#     return render_template('payment/payment.html')
#
# @connecsiApp.route('/checkout')
# @is_logged_in
# def checkout():
#     return redirect(url_for('viewMyPayments'))
#
@connecsiApp.route('/viewMyPayments')
@is_logged_in
def viewMyPayments():
    data = ''
    user_id = session['user_id']
    url = base_url + 'Payments/'+str(user_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print(data)
        return render_template('user/view_my_payments.html', data=data)
    except:
        pass
    return render_template('user/view_my_payments.html',data=data)


@connecsiApp.route('/addCampaign')
@is_logged_in
def addCampaign():
    addCampaign.counter+=1
    if addCampaign.counter==1:
        url_regionCodes = base_url + 'Youtube/regionCodes'
        regionCodes_json = ''
        try:
            regionCodes_response = requests.get(url=url_regionCodes)
            regionCodes_json = regionCodes_response.json()
            print(regionCodes_json)
        except:pass
        url_videoCat = base_url + 'Youtube/videoCategories'
        videoCat_json=''
        try:
            response_videoCat = requests.get(url=url_videoCat)
            videoCat_json = response_videoCat.json()
            print(videoCat_json)
        except Exception as e:
            print(e)
        return render_template('campaign/add_campaignForm.html',regionCodes=regionCodes_json,videoCategories = videoCat_json)
    else:
        addCampaign.counter=0
        return ''
addCampaign.counter=0


@connecsiApp.route('/viewCampaigns',methods=['GET','POST'])
@is_logged_in
def viewCampaigns():
    viewCampaigns.counter+=1
    print('view campaigns function',viewCampaigns.counter)
    if viewCampaigns.counter==1:
        user_id=session['user_id']
        view_campaign_data = ''
        url_view_campaigns = base_url + 'Campaign/'+ str(user_id)
        try:
            view_campaigns_response = requests.get(url=url_view_campaigns)
            view_campaign_data = view_campaigns_response.json()
            # print(view_campaign_data)
            for item in view_campaign_data['data']:
                # print(item)
                region_id_list = item['regions'].split(',')
                region_name_list=[]
                for region_id in region_id_list:
                    try:
                        region_name_response=requests.get(url=base_url+'Youtube/regionCode/'+str(region_id))
                        region_data = region_name_response.json()
                        region_name=region_data['data'][0][1]
                        region_name_list.append(region_name)
                    except:pass
                cat_response=requests.get(url=base_url+'Youtube/videoCategories/'+str(item['video_cat_id']))
                # print(cat_response.json())
                cat_json_data=cat_response.json()
                video_cat_name=cat_json_data['data'][0]['video_cat_name']
                item.update({'video_cat_name':video_cat_name})
                item.update({'region_name_list': region_name_list})
                try:
                    string_from_date= datetime.datetime.strptime(item['from_date'], '%Y-%m-%d')
                    string_from_date=string_from_date.strftime('%d-%b-%y')
                    string_to_date = datetime.datetime.strptime(item['to_date'], '%Y-%m-%d')
                    string_to_date = string_to_date.strftime('%d-%b-%y')
                    item.update({'from_date':string_from_date})
                    item.update({'to_date': string_to_date})
                except Exception as e:
                    print(e)

            print('campaign data',view_campaign_data)
            viewCampaigns.counter = 0
            return render_template('campaign/viewCampaigns.html',view_campaign_data=view_campaign_data),view_campaign_data
        except Exception as e:
            flash('Data loaded','success')
        viewCampaigns.counter = 0
        return render_template('campaign/viewCampaigns.html',view_campaign_data=view_campaign_data),view_campaign_data
    else:
         viewCampaigns.counter=0
         return ''
viewCampaigns.counter=0


@connecsiApp.route('/viewCampaignDetails/<string:campaign_id>',methods=['GET'])
@is_logged_in
def viewCampaignDetails(campaign_id):
    user_id = session['user_id']
    view_campaign_details_data = ''
    url_view_campaign_details = base_url + 'Campaign/'+str(campaign_id)+'/' + str(user_id)
    try:
        view_campaigns_response = requests.get(url=url_view_campaign_details)
        view_campaign_details_data = view_campaigns_response.json()
        print(view_campaign_details_data)
        return render_template('campaign/viewCampaignDetails.html',view_campaign_details_data=view_campaign_details_data)
    except Exception as e:
        flash('Error is Getting Data From Backend Please try again Later')
    return render_template('campaign/viewCampaignDetails.html',view_campaign_details_data=view_campaign_details_data)


@connecsiApp.route('/saveCampaign',methods=['POST'])
@is_logged_in
def saveCampaign():
    if request.method == 'POST':
        payload = request.form.to_dict()
        print(payload)
        channels = request.form.getlist('channels')
        channels_string = ','.join(channels)
        payload.update({'channels':channels_string})
        regions = request.form.getlist('country')
        regions_string = ','.join(regions)
        payload.update({'regions':regions_string})


        arrangements = request.form.getlist('arrangements')
        arrangements_string = ','.join(arrangements)
        payload.update({'arrangements': arrangements_string})

        is_classified_post = request.form.get('is_classified_post')
        print('is classified = ',is_classified_post)
        try:
            del payload['country']
            del payload['is_classified_post']
        except:pass
        if is_classified_post == 'on':
            payload.update({'is_classified_post':'TRUE'})
        else:
            payload.update({'is_classified_post':'FALSE'})
        print(payload)
        # exit()
#
#         files = request.form.getlist('files')
#         # files = request.files.getlist("files")
#         print(files)
#
        user_id = session['user_id']
        url = base_url + 'Campaign/' + str(user_id)
        try:
            response = requests.post(url=url, json=payload)
            result_json = response.json()
            print(result_json)
            flash('saved Campaign', 'success')
            return viewCampaigns()
        except:
            pass
    else:
        flash('Unauthorized', 'danger')


@connecsiApp.route('/calenderView')
@is_logged_in
def calendarView():
    return render_template('campaign/calenderView.html')

@connecsiApp.route('/inbox/<string:message_id>',methods = ['GET'])
@is_logged_in
def inbox(message_id):
    message_id = str(message_id)
    inbox = ''
    full_conv=''
    conv_title=''
    length_conv=''
    user_id = session['user_id']
    type = session['type']
    email_id = session['email_id']
    url = base_url + 'Messages/' + str(user_id) + '/' + type
    conv_url = base_url + 'Messages/conversations/' + str(email_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        print('messages = ',data)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        print('conv = ',conv_data)
        ###################### get inbox
        inboxList=[]
        for item in data['data']:
            if item['to_email_id'] == email_id:
               inboxList.append(item)
        # print(mylist)
        for item in conv_data['data']:
            if item['to_email_id'] == email_id:
               inboxList.append(item)
        inbox = {}
        inbox.update({'data':inboxList})
        print('inbox = ',inbox)

        for item in inbox['data']:
            inbox_user_id = item['user_id']
            # print(inbox_user_id)
            inbox_user_type = item['user_type']
            first_name = ''
            if inbox_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(inbox_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                first_name = brand_details_json['data']['first_name']
            elif inbox_user_type == 'influencer':
                influencer_details_url = base_url + '/Influencer/' + str(inbox_user_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                first_name = influencer_details_json['data']['first_name']
            item.update({'first_name': first_name})
            # print(item)

        # #######################################

        from_email_id=''
        if message_id == "0":
            try:
                message_id = inbox['data'][0]['message_id']
                from_email_id = inbox['data'][0]['from_email_id']
                print('default message id = ', message_id)
            except:pass
        else: print('new message id = ',message_id)
            # print(from_email_id)
        # ########################### get conversations

        getConv_url = base_url + 'Messages/conversations/' + str(message_id)+'/'+str(user_id)+'/'+str(type)
        print(getConv_url)
        full_conv_resposne = requests.get(url=getConv_url)
        full_conv_data = full_conv_resposne.json()
        print('full_conv_data = ',full_conv_data)
        #################################################
        convList = []
        for item in data['data']:
            if item['message_id'] == int(message_id):
                convList.append(item)
        # print(mylist)
        for item in full_conv_data['data']:
            if item['message_id'] == int(message_id):
                convList.append(item)
        full_conv = {}
        full_conv.update({'data': convList})
        print('full_conv = ', full_conv)
        length_conv = len(full_conv['data'])
        print('length = ',length_conv)
        collapse_id = 1
        for item in full_conv['data']:
            full_conv_user_id = item['user_id']
            # print(full_conv_user_id)
            full_conv_user_type = item['user_type']
            first_name = ''
            if full_conv_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(full_conv_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                first_name = brand_details_json['data']['first_name']
            elif full_conv_user_type == 'influencer':
                influencer_details_url = base_url + '/Influencer/' + str(full_conv_user_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                first_name = influencer_details_json['data']['first_name']
            item.update({'first_name': first_name})
            item.update({'collapse_id':collapse_id})
            # print(item)
            collapse_id+=1
################ remove deleted message from inbox and conv ##################
        removed_deleted_messages_from_inbox = []
        for item in inbox['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                print('deleted user list from inbox',deleted_from_user_id_list)
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_inbox.append(item)
            except:
                removed_deleted_messages_from_inbox.append(item)
                pass
        inbox.update({'data': removed_deleted_messages_from_inbox})
        print('removed deleted from inbox', inbox)

        removed_deleted_messages_from_conv = []
        for item in full_conv['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                print('deleted user list from full conv', deleted_from_user_id_list)
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_conv.append(item)
            except:
                removed_deleted_messages_from_conv.append(item)
                pass
        full_conv.update({'data':removed_deleted_messages_from_conv})
        print('removed deleted from conv',full_conv)
############################################################
        # ####################################
        try:
            conv_title = full_conv['data'][0]['subject']
        except:pass
        return render_template('email/inbox.html', inbox = inbox, full_conv = full_conv, conv_title=conv_title)
    except:
        pass
    return render_template('email/inbox.html',inbox=inbox, full_conv = full_conv,conv_title=conv_title)



@connecsiApp.route('/deleted',methods = ['GET'])
@is_logged_in
def deleted():
    deleted_dict=''
    user_id = session['user_id']
    type = session['type']
    email_id = session['email_id']
    url = base_url + 'Messages/' + str(user_id) + '/'+ type
    conv_url = base_url + 'Messages/conversations/all/'+type
    print(conv_url)
    # conv_url = base_url + 'Messages/conversations/' + str(email_id)
    try:
        response = requests.get(url=url)
        messages = response.json()
        print('messages = ',messages)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        print('conv = ',conv_data)
        # exit()
        ###################### get inbox
        deleted_list=[]
        for item in messages['data']:
            if item['deleted'] == 'true':
               deleted_list.append(item)
        # print(mylist)
        for item in conv_data['data']:
            if item['deleted'] == 'true':
               deleted_list.append(item)
        deleted_dict = {}
        deleted_dict.update({'data':deleted_list})
        print('deleted dict = ',deleted_dict)
        # exit()

        # ########################### get conversations
        collapse_id = 1
        for item in deleted_dict['data']:
            full_conv_user_id = item['user_id']
            # print(full_conv_user_id)
            full_conv_user_type = item['user_type']
            first_name = ''
            if full_conv_user_type == 'brand':
                brand_details_url = base_url+'/Brand/'+str(full_conv_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                first_name = brand_details_json['data']['first_name']
            elif full_conv_user_type == 'influencer':
                influencer_details_url = base_url + '/Influencer/' + str(full_conv_user_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                first_name = influencer_details_json['data']['first_name']
            item.update({'first_name': first_name})
            item.update({'collapse_id':collapse_id})
            # print(item)
            collapse_id+=1

################ remove deleted message from inbox and conv ##################
        removed_deleted_messages_from_conv = []
        for item in deleted_dict['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                print('deleted user list', deleted_from_user_id_list)
                if str(user_id) in deleted_from_user_id_list:
                    removed_deleted_messages_from_conv.append(item)
            except Exception as e:
                removed_deleted_messages_from_conv.append(item)
                pass
                print(e)
        deleted_dict.update({'data':removed_deleted_messages_from_conv})
        print('deleted messages',deleted_dict)
############################################################
        # ####################################
        return render_template('email/deleted.html', deleted_dict = deleted_dict)
    except:
        pass
    return render_template('email/deleted.html',deleted_dict = deleted_dict)




@connecsiApp.route('/sent',methods = ['GET'])
@is_logged_in
def sent():
    sent = ''
    user_id = session['user_id']
    type = session['type']
    email_id = session['email_id']
    url = base_url + 'Messages/' + str(user_id) + '/' + type
    conv_url = base_url + 'Messages/conversations/sent/' + str(email_id)
    try:
        response = requests.get(url=url)
        data = response.json()
        # print('messages = ', data)
        conv_resposne = requests.get(url=conv_url)
        conv_data = conv_resposne.json()
        # print('conv = ', conv_data)
        ###################### get sent
        sentList = []
        for item in data['data']:
            if item['from_email_id'] == email_id:
                sentList.append(item)
        # print(mylist)
        for item in conv_data['data']:
            if item['from_email_id'] == email_id:
                sentList.append(item)

        sent = {}
        sent.update({'data': sentList})
        # print('sent = ', sent)

        collapse_id = 1
        for item in sent['data']:
            sent_user_id = item['user_id']
            # print(sent_user_id)
            sent_user_type = item['user_type']
            first_name = ''
            if sent_user_type == 'brand':
                brand_details_url = base_url + '/Brand/' + str(sent_user_id)
                brand_details_resposne = requests.get(url=brand_details_url)
                brand_details_json = brand_details_resposne.json()
                # print(brand_details_json)
                first_name = brand_details_json['data']['first_name']
            elif sent_user_type == 'influencer':
                influencer_details_url = base_url + '/Influencer/' + str(sent_user_id)
                influencer_details_resposne = requests.get(url=influencer_details_url)
                influencer_details_json = influencer_details_resposne.json()
                # print(influencer_details_json)
                first_name = influencer_details_json['data']['first_name']
            item.update({'first_name': first_name})
            item.update({'collapse_id': collapse_id})
            # print(item)
            collapse_id += 1

        removed_deleted_messages_from_sent = []
        for item in sent['data']:
            try:
                deleted_from_user_id_string = item['deleted_from_user_id']
                deleted_from_user_id_list = deleted_from_user_id_string.split(',')
                if str(user_id) not in deleted_from_user_id_list:
                    removed_deleted_messages_from_sent.append(item)
            except:
                pass
        sent.update({'data': removed_deleted_messages_from_sent})
        print('removed deleted', sent)

        return render_template('email/sent.html', sent=sent)
    except:
        pass
    return render_template('email/sent.html', sent=sent)




@connecsiApp.route('/delete/<string:message_id>/<string:conv_id>/<string:user_id>', methods = ['GET'])
@is_logged_in
def delete(message_id,conv_id,user_id):
    # print(message_id,conv_id)
    conv_id = int(conv_id)
    # print(type(conv_id))
    print(user_id)
    if conv_id != 0:
        url_delete_msg_from_conv = base_url+'Messages/conversations/delete/'+str(message_id)+'/'+str(conv_id)+'/'+str(user_id)
        print(url_delete_msg_from_conv)
        response = requests.put(url=url_delete_msg_from_conv)
        print(response.json())
        flash('message moved to deleted', 'warning')
        return redirect(url_for('admin'))
    else:
        url_delete_msg_from_messages = base_url+'Messages/delete/'+str(message_id)+'/'+str(user_id)
        print(url_delete_msg_from_messages)
        response = requests.put(url=url_delete_msg_from_messages)
        print(response.json())
        flash('message moved to deleted', 'warning')
        return redirect(url_for('admin'))


@connecsiApp.route('/compose')
@is_logged_in
def compose():
    return render_template('email/compose.html')

@connecsiApp.route('/reply/<string:message_id>/<string:to_email_id>/<string:subject>',methods = ['GET'])
@is_logged_in
def reply(message_id,to_email_id,subject):
    return render_template('email/reply.html',to_email_id=to_email_id,subject=subject,message_id=message_id)


@connecsiApp.route('/sendEmail',methods = ['POST'])
@is_logged_in
def sendEmail():
    if request.method == 'POST':
       payload = request.form.to_dict()
       # print(payload)
       payload.update({'from_email_id': session['email_id']})
       # print(payload)
       date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
       payload.update({'date':date})
       print(payload)
       user_id= session['user_id']
       type = session['type']
       url = base_url + 'Messages/' + str(user_id) +'/' + type
       try:
           response = requests.post(url=url, json=payload)
           data = response.json()
           print(data)
           flash('Your email has been sent', category='success')
           return render_template('email/inbox.html', data=data)
       except:
           pass
       return render_template('email/compose.html')

@connecsiApp.route('/replyEmail/<string:message_id>', methods=['POST'])
@is_logged_in
def replyEmail(message_id):
    if request.method == 'POST':
        payload = request.form.to_dict()
        # print(payload)
        payload.update({'conv_from_email_id': session['email_id']})
        # print(payload)
        date = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
        payload.update({'date': date})
        print(payload)
        user_id = session['user_id']
        type = session['type']
        url = base_url + 'Messages/conversations/' +str(message_id)+'/'+ str(user_id) + '/' + type
        print(url)
        # exit()
        try:
            response = requests.post(url=url, json=payload)
            data = response.json()
            print(data)
            flash('Your email has been sent', category='success')
            return render_template('email/inbox.html', data=data)
        except:
            pass
        return render_template('email/compose.html')


@connecsiApp.route('/test')
@is_logged_in
def test():
    return render_template('testRequest.html')


@connecsiApp.route('/addToFavInfList/<string:channel_id>',methods=['GET'])
@is_logged_in
def addToFavInfList(channel_id):
    addToFavInfList.counter += 1
    # print(addToFavInfList.counter)
    if addToFavInfList.counter==1:
        try:
            print(channel_id)
            user_id = session['user_id']
            # print('user_id=',user_id)
            url = base_url+'/Brand/addToFavList/'+channel_id+'/'+str(user_id)
            response = requests.post(url=url)
            # data = response.json()
            flash("Added to Favorites List", 'success')
            return searchInfluencers()
            # return ''
        except:
            pass
            flash("Could not be added to Favorites List", 'danger')
            return influencerFavoritesList()
    else:
        addToFavInfList.counter = 0
        return influencerFavoritesList()
addToFavInfList.counter=0


@connecsiApp.route('/influencerFavoritesList')
@is_logged_in
def influencerFavoritesList():
    data=''
    try:
        user_id = session['user_id']
        url = base_url+'/Brand/getInfluencerFavList/'+str(user_id)
        response = requests.get(url=url)
        data = response.json()
        linechart_id = 1
        for item in data['data']:
            item.update({'linechart_id': linechart_id})
            print(item)
            linechart_id += 1
        return render_template('partnerships/influencerFavoritesList.html',data=data),data
    except:
        pass
        return render_template('partnerships/influencerFavoritesList.html'),data

@connecsiApp.route('/createAlerts', methods=['POST'])
@is_logged_in
def createAlerts():
    user_id=session['user_id']
    if request.method == 'POST':
        payload = request.form.to_dict()
        print(payload)
        try:
            url = base_url + '/Brand/createInfluencerAlerts/'+str(user_id)
            response = requests.put(url=url,json=payload)
            # data = response.json()
            flash("Created Alerts for Favorite Influencer", 'success')
            return influencerFavoritesList()
        except:
            pass
            flash("Error in Creating Alerts", 'danger')
            return influencerFavoritesList()

@connecsiApp.route('/viewAllClassifiedAds')
@is_logged_in
def viewAllClassifiedAds():
    return render_template('classifiedAds/view_all_classifiedAds.html')

@connecsiApp.route('/viewClassifiedDetails')
@is_logged_in
def viewClassifiedDetails():
    return render_template('classifiedAds/viewClassifiedDetails.html')

############################################## influencer Section###########################################################

@connecsiApp.route('/inf_profile')
@is_logged_in
def inf_profile():
    return render_template('user/inf_profile.html')

@connecsiApp.route('/inf_editProfile')
@is_logged_in
def inf_editProfile():
    return render_template('user/inf_editProfile.html')

        # @connecsiApp.route('/login/authorized')
# def authorized():
#     resp = linkedin.authorized_response()
#     if resp is None:
#         return 'Access denied: reason=%s error=%s' % (
#             request.args['error_reason'],
#             request.args['error_description']
#         )
#     session['linkedin_token'] = (resp['access_token'], '')

    # me = linkedin.get('people/~')
    # email_linkedin = linkedin.get('people/~:(email-address)')
    # print(jsonify(email_linkedin.data))

    # email_id = email_linkedin.data['emailAddress']
    # data=[me.data['id'],me.data['firstName'],me.data['lastName'],email_id,'',me.data['headline'],'Admin']
    # print(me.data)
    # session['logged_in'] = True
    # session['type'] = 'brand'
    # session['user_id'] = me.data['id']
    # session['first_name']=me.data['firstName']
    # print(data)
    # return render_template('index.html',data=data)

# @linkedin.tokengetter
# def get_linkedin_oauth_token():
#     return session.get('linkedin_token')


# def change_linkedin_query(uri, headers, body):
#     auth = headers.pop('Authorization')
#     headers['x-li-format'] = 'json'
#     if auth:
#         auth = auth.replace('Bearer', '').strip()
#         if '?' in uri:
#             uri += '&oauth2_access_token=' + auth
#         else:
#             uri += '?oauth2_access_token=' + auth
#     return uri, headers, body
#
# linkedin.pre_request = change_linkedin_query

if __name__ == '__main__':
    # connecsiApp.secret_key = 'connecsiSecretKey'
    connecsiApp.run(debug=True,host='localhost')
