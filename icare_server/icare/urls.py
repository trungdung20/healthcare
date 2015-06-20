from __future__ import unicode_literals
from django.conf.urls import patterns, url 
from icare import views



from endless_pagination.decorators import (
    page_template,
    page_templates,
)

urlpatterns = patterns('',
		#home and index 
		url(r'^$',views.intro, name='intro'),
		url(r'^login/$', views.intro_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^index/$',page_template('icare/content/question_index_page.html')(views.index),{'template':'icare/content/question_index.html'},name='index'),
		#question contetn 
		url(r'^question/post/$', views.question_post, name='question_post'),
		url(r'^question/show/(?P<question_id>\w+)/$',page_template('icare/content/question_show_page.html')(views.question_show),{'template':'icare/content/question_show.html'}, name='question'),
		url(r'^question/answer/(?P<question_id>\w+)/$',views.question_answer, name='question_answer'),
		url(r'^agree_answer/$', views.answer_agree, name='answer_agree'),
		url(r'^thanks_answer/$', views.answer_thanks, name='answer_thanks'),
		#checklist contents 
		url(r'^category/$', views.category_show, name = 'category_show'),
		url(r'^(?P<goal_id>\w+)/check_lists/$',page_template('icare/content/checklist_index_page.html')(views.checklist_index),{'template':'icare/content/checklist_index.html'}, name = 'checklist_index'),
		url(r'^checklist/my_checklist/(?P<user_id>\w+)/$',page_template('icare/patient/user_checklist_index_page.html')(views.checklist_person),{'template':'icare/patient/user_checklist_index.html'}, name='checklist_person'),
		url(r'^checklist/thanks_checklist/$', views.thanks_checklist, name="thanks_checklist"),
		url(r'^checklist/doctor_add_checklist/(?P<topic_id>\w+)/$', views.checklist_doctor_add, name="checklist_doctor_add"),
		url(r'^item/edit/(?P<checklist_id>\w+)/$', views.doctor_edit_checklist,name="doctor_edit_checklist"),
		url(r'^item/add/$',views.item_add,name="add_item"),
		url(r'^item/submit/(?P<checklist_id>\w+)/$',views.item_submit, name="item_submit"),
		url(r'^item/delete/$',views.item_delete,name="item_delete"),
		url(r'^checklist/patient_add_checklist/$', views.add_checklist, name="add_checklist"),
		url(r'^checklist/agree_checklist/$', views.agree_checklist, name="agree_checklist"),
		url(r'^user_checklist_item/complete/$',views.item_complete, name="item_complete"),
		url(r'^patient_checklist/delete/$', views.checklist_delete, name="checklist_delete"),
		#user follow topic 
		url(r'^user/topic/follow/$',views.topic_follow,name="topic_follow"),
		
		#link for topics 
		url(r'topic/show/(?P<topic_id>\w+)/$',page_template('icare/content/topic_show_page.html')(views.topic_show),{'template':'icare/content/topic_show.html'},name='topic_show'),
		url(r'topic/add/$',views.topic_add, name='topic_add'),
		url(r'topic/add/related_topic/(?P<topic_id>\w+)/$',views.add_related_topic,name="add_related_topic"),
		url(r'topic/edit/(?P<topic_id>\w+)/$', views.topic_edit,name='topic_edit'),
		#link for seach index 
		url(r'^search/$', views.search_index , name='search_index'),
		url(r'^search/condition/result/$',page_template('icare/search/search_condition_page.html')(views.search_condition_result),{'template':'icare/search/search_condition.html'}, name='search_condition_result'),
		url(r'^search/condition/$', page_template('icare/search/search_condition_all_page.html')(views.search_condition),{'template':'icare/search/search_condition.html'}, name='search_condition'),
		url(r'^search/symptom/$', page_template('icare/search/search_symptom_all_page.html')(views.search_symptom),{'template':'icare/search/search_symptom.html'}, name='search_symptom'),
		url(r'^search/symptom/result/$', page_template('icare/search/search_symptom_page.html')(views.search_symptom_result),{'template':'icare/search/search_symptom.html'}, name='search_symptom_result'),
		url(r'^search/medication/$',page_template('icare/search/search_medication_all_page.html')(views.search_medication),{'template':'icare/search/search_medication.html'}, name='search_medication'),
		url(r'^search/medication/result/$',page_template('icare/search/search_medication_page.html')(views.search_medication_result),{'template':'icare/search/search_medication.html'}, name='search_medication_result'),
		url(r'^search/procedure/$',page_template('icare/search/search_procedure_all_page.html')(views.search_procedure),{'template':'icare/search/search_procedure.html'}, name='search_procedure'),
		url(r'^search/procedure/result/$',page_template('icare/search/search_procedure_page.html')(views.search_procedure_result),{'template':'icare/search/search_procedure.html'}, name='search_procedure_result'),
		url(r'^search/doctor/$',page_template('icare/search/search_doctor_all_page.html')(views.search_doctor),{'template':'icare/search/search_doctor.html'}, name='search_doctor'),
		url(r'^search/doctor/result/$',page_template('icare/search/search_doctor_page.html')(views.search_doctor_result),{'template':'icare/search/search_doctor.html'}, name='search_doctor_result'),
		url(r'^search/patient/$',page_template('icare/search/search_patient_all_page.html')(views.search_patient),{'template':'icare/search/search_patient.html'}, name='search_patient'),
		url(r'^search/patient/result/$',page_template('icare/search/search_patient_page.html')(views.search_patient_result),{'template':'icare/search/search_patient.html'}, name='search_patient_result'),
		#account seeting 
		url(r'^account_setting/$',views.user_changepass,name="user_changepass"),
		
		url(r'^thank_checklist/$',views.thanks_checklist, name='thank_checklist'),
		url(r'^add_checklist/$', views.add_checklist, name='add_checklist'),
		url(r'^agree_checklist/$',views.agree_checklist, name='agree_checklist'),
		#login and register 
        url(r'^register/$',views.register, name='register'),
		url(r'^register/doctor/$', views.register_doctor, name='register_doctor'),
		url(r'^register/patient/$', views.register_patient, name='register_patient'),
		#post question in topic 
		url(r'^question/post/topic/(?P<topic_id>\w+)/$',views.post_question_topic,name="post_question_topic"),
		url(r'^profile/doctor/(?P<doctor_id>\w+)/$', views.profile_doctor, name='profile_doctor'),
		url(r'^profile/doctor/edit/(?P<doctor_record_id>\w+)/$',views.doctor_edit_profile,name='doctor_edit_profile'),
		url(r'^profile/patient/(?P<patient_id>\w+)/$', views.profile_patient, name='profile_patient'),
		# doctor and patient relation 
		url(r'^patient_care_list_request/$', views.patient_send_request, name='patient_send_request'),
		url(r'^doctor_care_list_request/$', views.doctor_send_request, name='doctor_send_request'),
		url(r'^health_care_list/doctor_list/$', views.patient_friend_list, name='patient_friend_list'),
		url(r'^health_care_list/patient_list/$', views.doctor_friend_list, name='doctor_friend_list'),
		#change privacy question 
		url(r'^patient/question/private/$',views.patient_question_private,name="patient_question_private"),
		url(r'^patient/question/public/$',views.patient_question_public,name="patient_question_public"),
		
		url(r'^notification/doctor/$', views.doctor_notification_request, name='doctor_notification_request'),
		url(r'^notification/patient/$', views.patient_notification_request, name='patient_notification_request'),
		
		url(r'^request/patient/send/advisor_request/$',views.handle_patient_advisor_request,name='handle_patient_advisor_request'),
		url(r'^request/accept/doctor/$',views.doctor_friend_accept, name='doctor_friend_accept'), # handles friend request made by doctor accept
		url(r'^request/accept/patient/$', views.patient_friend_accept, name='patient_friend_accept'), # handles friend request made by patient accept 
		url(r'^request/reject/doctor/$', views.doctor_friend_reject, name='doctor_friend_reject'), # handles friend request made by doctor reject 
		url(r'^request/reject/patient/$', views.patient_friend_reject, name='patient_friend_reject' ), # handles friend request made by patient reject
		url(r'^patient/view_rejected.request/$',views.patient_view_rejected_request,name="patient_view_rejected_request"),
		url(r'^patient/view_accepted_request/$',views.patient_view_accepted_request,name='patient_view_accepted_request'),
		url(r'^patient/doctor_advisor_accepted/$',views.patient_accepted_advisor_request,name='patient_accepted_advisor'),
		url(r'^patient/doctor_advisor_rejected/$',views.patient_rejected_advisor_request,name='patient_rejected_advisor'),
		url(r'^patient/doctor_answer_alert/$',views.patient_doctor_answer_alert,name='patient_doctor_answer_alert'),
		url(r'^patient/reject_current_advisor/$',views.patient_reject_current_advisor,name="patient_reject_current_advisor"),
		
		url(r'^doctor/view_accepted_request/$',views.doctor_view_accepted_request,name="doctor_view_accepted_request"),
		url(r'^doctor/view_rejected_request/$',views.doctor_view_rejected_request,name="doctor_view_accepted_request"),
		url(r'^doctor/patient_advisor_reject/$',views.doctor_view_advisor_reject,name="doctor_view_advisor_request"),
		url(r'^doctor/patient_advisor_accept/$',views.doctor_view_advisor_accept,name="doctor_view_advisor_request"),
		url(r'^doctor/patient_question_alert/$',views.doctor_view_question_alert,name="doctor_view_question_alert"),
		url(r'^patient/doctor/advisor/(?P<patient_id>\w+)/$',page_template('icare/patient/patient_advisor_tab_page.html')(views.patient_view_advisor),{'template':'icare/patient/patient_advisor_tab.html'},name="patient_view_advisor"),
		url(r'^question/patient/post/advisor/(?P<doctor_id>\w+)/$',views.question_post_to_advisor,name="question_post_to_advisor"),
		url(r'^doctor/patient/advised/(?P<doctor_id>\w+)/$',views.doctor_advisor_tab_manage,name="doctor_Advisor_tab_manage"),
		url(r'^doctor/advised/patient/profile/(?P<patient_id>\w+)/$',views.doctor_manage_advised_patient,name="doctor_manage_advised_patient"),
		url(r'^doctor/advisor/question/answer/(?P<question_id>\w+)/$',views.doctor_answer_to_advisor,name="doctor_answer_to_advisor"),
		
		url(r'^patient/weight/edit/$', views.patient_edit_weight, name='patient_edit_weight'), # pull out weight edit form 
		url(r'^patient/weight/edit_submit/(?P<patient_record_id>\w+)/$', views.patient_edit_submit_weight, name='patient_edit_submit_weight'), # submit weight patient form 
		url(r'^patient/height/edit/$',views.patient_edit_height, name='patient_edit_height'),
		url(r'^patient/height/edit_submit/(?P<patient_record_id>\w+)/$', views.patient_edit_submit_height, name='patient_edit_submit_height'),
		url(r'^patient/ethnicity/edit/$',views.patient_edit_ethnicity,name="patient_edit_ethnicity"),
		url(r'^patient/ethnicity/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_ethnicity,name='patient_edit_submit_ethnicity'),
		url(r'^patient/vaccination/edit/$',views.patient_edit_vaccination, name="patient_edit_vaccination"),
		url(r'^patient/vaccination/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_vaccination, name="patient_edit_submit_vaccination"),
		url(r'^patient/dietary/edit/$',views.patient_edit_dietary, name='patient_edit_dietary'),
		url(r'^patient/dietary/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_dietary, name='patient_edit_submit_dietary'),
		url(r'^patient/alcohol/edit/$',views.patient_edit_alcohol,name='patient_edit_alcohol'),
		url(r'^patient/alcohol/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_alcohol,name='patient_edit_submit_alcohol'),
		url(r'^patient/tobacco/edit/$',views.patient_edit_tobacco,name='patient_edit_tobacco'),
		url(r'^patient/tobacco/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_tobacco,name='patient_edit_submit_tobacco'),
		url(r'^patient/sex/edit/$',views.patient_edit_sex,name="patient_edit_sex"),
		url(r'^patient/sex/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_sex,name="sex"),
		url(r'^patient/recreational_drug/edit/$',views.patient_edit_drug, name="patient_edit_drug"),
		url(r'^patient/recreational_drug/edit_submit/(?P<patient_record_id>\w+)/$',views.patient_edit_submit_drug, name='patient_edit_submit_drug'),
	)
