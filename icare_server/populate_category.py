# -*- coding: utf-8 -*-
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','icare_server.settings')
import django 
django.setup()

from django.contrib.auth.models import User
from icare.models import Category, Goal, Topic, Medication, Vaccination, Condition , Symptom , Procedure, Riskfactor, Doctor ,ListItem, CheckList,Notification,DoctorRecord ,Question,Answer,QuestionAndTopic,QuestionRelate,TopicAndGoal

def populate():
	#add category 
	improve_health = category_add(title="Improving Health")
	manage_condition = category_add(title="Manage a Condition")
	parenting_pregnancy = category_add(title="Parenting and Pregnancy")
	grow_up = category_add(title="Growing up")
	
	#add goal 
	healthy_diet = goal_add("Eating a Healthy Diet", improve_health)
	losing_weight = goal_add("Losing Weight",improve_health)
	getting_fit = goal_add("Getting Fit",improve_health)
	sleeping_better = goal_add("Seeping Better",improve_health)
	improving_heart_health = goal_add("Improving Heart Health", improve_health)
	quit_smoking = goal_add("Quitting smoking",improve_health)
	improving_relationships = goal_add("Improving Relationships",improve_health)
	healthy_traveling = goal_add("Staying Healthy While Travelling",improve_health)
	healthy_woman = goal_add("Being a healthy Woman",improve_health)
	healthy_man = goal_add("Being a healthy Man",improve_health)
	
	deal_emesis = goal_add("Dealing with Emesis",manage_condition)
	abnormal_heart_rhythm = goal_add("Treating an Abnormal Heart Rhythm", manage_condition)
	accidental_poisoning =goal_add("Treating Accidental Poisoning",manage_condition)
	manage_acne = goal_add("Managing Acne",manage_condition)
	treating_acute_bronchitis = goal_add("Treating Acute Bronchitis",manage_condition)
	living_add_adhd = goal_add("Living with ADD/ADHD",manage_condition)
	overcoming_addiction = goal_add("Overcoming Addiction",manage_condition)
	living_aids = goal_add("Living with AIDS",manage_condition)
	manage_anger = goal_add("Managing Anger",manage_condition)
	taking_antibio = goal_add("Taking Antibiotics",manage_condition)
	overcome_stress = goal_add("Overcoming Anxiety and Stress",manage_condition)
	back_pain = goal_add("Managing Back Pain",manage_condition)
	broken_bone = goal_add("Recovering form a Broken Bone",manage_condition)
	treat_burn = goal_add("Treating Burn",manage_condition)
	treat_cold = goal_add("Treating a Cold", manage_condition)
	treat_constipation = goal_add("Treating Constipation", manage_condition)
	copd = goal_add("Living with COPD", manage_condition)
	diarrhea = goal_add("Treating Diarrhea", manage_condition)
	dry_skin = goal_add("Treating Dry Skin", manage_condition)
	ear_infection = goal_add("Treating Ear Infection", manage_condition)
	overcome_fatigue = goal_add("Overcoming Fatigue",manage_condition)
	treating_fever = goal_add("Treating a Fever", manage_condition)
	manage_glaucoma = goal_add("Managing Glaucoma", manage_condition)
	treat_headache = goal_add("Treating Headaches", manage_condition)
	treat_heart_stroke = goal_add("Treating Heat Stroke", manage_condition)
	overcome_insomnia = goal_add("Overcoming Insomnia", manage_condition)
	manage_knee_pain = goal_add("Managing Kidney Stones",manage_condition)
	
	caregiving = goal_add("Caregiving for a Spouse", parenting_pregnancy)
	miscarriage = goal_add("Coping with a Miscarriage", parenting_pregnancy)
	healthy_pregnancy = goal_add("Having Healthy Pregnancy", parenting_pregnancy)
	try_conceive = goal_add("Trying to Conceive", parenting_pregnancy)
	breastfeeding = goal_add("Breastfeeding Your Child", parenting_pregnancy)
	care_baby = goal_add("Caring for Your Baby", parenting_pregnancy)
	care_toddler = goal_add("Caring for Your Toddler",parenting_pregnancy)
	care_teen = goal_add("Caring for Tweens & Teens", parenting_pregnancy)
	care_preemie = goal_add("Caring for a Preemie", parenting_pregnancy)
	care_puberty = goal_add("Parenting a Child During Puberty", parenting_pregnancy)
	care_disorder = goal_add("Parenting a Child with a Learning Disorder", parenting_pregnancy)
	prevent_pregnancy = goal_add("Preventing Pregnancy",parenting_pregnancy)
	manage_infertility = goal_add("Managing Infertility",parenting_pregnancy)
	manage_pregnancy_complication = goal_add("Managing Pregnancy Complication",parenting_pregnancy)
	
	aging_graceful = goal_add("Ageing Gracefully",grow_up)
	understand_girl_purberty = goal_add("Understanding Puberty for Girls",grow_up)
	understand_boy_purberty = goal_add("Understanding Puberty for Boys",grow_up)
	preventing_fall = goal_add("Preventing Falls",grow_up)
	manage_hot_flashes = goal_add("Managing Hot Flashes",grow_up)
	irregular_periods = goal_add("Living with Irregular Periods",grow_up)
	male_menopause = goal_add("Managing Male Menopause", grow_up)
	memory_loss = goal_add("Living with Memory Loss",grow_up)
	hearing_loss = goal_add("Living with Hearing Loss",grow_up)
	
	
	
	#add doctor 
	
	email = 'dungbme10@gmail.com'
	password = '16041992'
	school = 'Test University'
	doctor1 = add_doctor('test1',email,password,'John Smith','Addiction Medicine','Male',school,'1234','MD',2010,'Test Address') 
	doctor2 = add_doctor('test2',email,password,'John Kennerdy','Cancer Surgery','Male',school,'12345','DO',2009,'Test Address') 
	doctor3 = add_doctor('test3',email,password,'Eva Braun','Radiation Oncology','Female',school,'123456','PharmD',2011,'Test Address') 
	doctor4 = add_doctor('test4',email,password,'Elizabeth Smith','Pediatric Cardiology','Female',school,'12345','MBBS',2011,'Test Address') 
	doctor5 = add_doctor('test5',email,password,'Christian Grey','Vascular Surgery','Female',school,'123455','MBBS',2011,'Test Address') 
	doctor6 = add_doctor('test6',email,password,'Garland Martin','Infectious Disease','Male',school,'12467','EdD',2010,'Test Address')
	doctor7 = add_doctor('test7',email,password,'Liesa Harte','Family Medicine','Female',school,'123890','DPM',2009,'Test Address')
	doctor8 = add_doctor('test8',email,password,'Gerard Honore','Neurology','Male',school,'12398','DDS',2007,'Test Address')
	doctor9 = add_doctor('test9',email,password,'Lori Semel','Sports Surgery','Female',school,'12346','MBBS',2006,'Test Address')
	doctor10 = add_doctor('test10',email,password,'Peri Suzan Gunay','Obstetrics and Gynecology','Female',school,'23450','EdD',2000,'Test Address')
	doctor11 = add_doctor('test11',email,password,'Peterson Pierre','Pediatric Cardiology','Male',school,'234457','PhD',2005,'Test Address')
	
	#add checklist 
	#eatting healthy diet checklist 
	topic1 = goal_add_sub(healthy_diet,'Low Carb Diet','A low-carb diet emphasis dietary protein and fats, but limits carbohydrates like grains, starchy vegetables and fruit.')
	topic2 = goal_add_sub(healthy_diet,'Healthy Diet','Pregnant women should eat a balanced, nutritional diet and increase their calorie intake to meet the needs of the developing fetus and their changing bodies. Eating a range of wholesome and nutritious foods during pregnancy is one of the most important things that women can do to ensure the normal development and growth of the fetus, and it can help to prevent prematurity and low birth weight. For the mother, good nutrition helps to prevent anemia, infection, and poor healing.')
	topic3 = goal_add_sub(healthy_diet,'Eat Healthier',"A good diet is central to overall good health. The new Healthy Eating Plate and Healthy Eating Pyramid shows the proportions and types of foods that promote healthier eating. It's all about getting back to the food basics. Look for alternatives to processed meat and other highly processed foods. Choose whole grains. Fill up your plate with colorful vegetables. Snack on fresh fruits. Your path to healthier eating can begin today.")
	
	question1 = add_question_goal(healthy_diet,"Is it possible that I lost 6 kg in a week? Or is the scale lying? Could it be that i'm now eating a healthy diet full of veggies and it will continue?")
	answer1 = add_answer(question1,doctor5,"That is 13.2 pounds and even if you are quite large, that would be unusual unless diuresis for heart failure, and a few other unusual items.")
	question1_related = add_question_sub(question1,"I am gaining weight. I need a diet plan to loose it. My weight is now 104 kg :(. I can't eat much as well, even i eat little - i feel that I am full.")
	answer1 = add_answer(question1_related,doctor7,"I've found a low carb (no starch or sugar) ketogenic diet containing about 80+rams of protein and below 50grams of carbohydrate along with mild exercise the most effective for weight, fat and girth loss.If you get in mild ketosis which is fat burning state your hunger level will be very little and you won't be starving yourself. I would suggest avoiding exercise the first week that you start the diet but after that you can exercise as much as you tolerate which will improve your weight-los.")
	question1_related = add_question_sub(question1,"What is the best diet pill on the market i'm exersing and eating healthy but i need a extra boost to help me lose 20 kg please?")
	answer1 = add_answer(question1_related,doctor8,"I don't recommend any of the pharmaceutical diet pills as they can have serious side effects.Certain herbs are proven to support weight loss, but only when combined with a healthy diet ; exercise- see http://bit.Ly/178bmuf re: your diet consider dr. Fuhrman's diet: http://bit.Ly/1dhw9ht dr. Weil has useful info: http://huff.To/19ygs8y- see his 'discuss that' link in his article.")
	answer2 = add_answer(question1_related,doctor9,"Diet pills are either ineffective or dangerous for the most part.If you are successfully losing weight (albeit slowly) on your current diet and exercise regimen, i would stick to that. This is the safest way to obtain weight loss that has the best chance of being a long-lasting phenomenon.")
	question1_related = add_question_sub(question1,"I have lost about 15 kg i don't have a fixed diet i run about 11 km a day on an elliptical trainer, now i'm stuck on 120 kg what can I do?")
	answer1 = add_answer(question1_related,doctor4,"Sometimes you lose inches instead of pounds as you convert fat to muscle.Keep eating a balanced diet watching portions and continue exercising. You may change up you exercise routine 1 or 2 times a week and see if this helps.")
	question1_related = add_question_sub(question1,"Where can you find information for vegetarians on eating a healthy diet?")
	answer1 = add_answer(question1_related,doctor8,"Internet, library, books, magazines, dietician, family doctor, county health department.")
	question1_related = add_question_sub(question1,"Am exercising and eating a healthy diet but i can't get rid o cellulite what should I do ?")
	answer1 = add_answer(question1_related,doctor6,"Cellulite can occur even in skinny people.Perhaps one of the newer type of laser techniques will help. Perhaps thermage will help. Very difficult to get rid of. Sometimes very superficial liposuction can help, but it i dangerous to the blood supply to the skin.")
	
	
	
	checklist_eating_healthy1 = add_checklist(healthy_diet,doctor1)
	item1_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Avoid fast food",'Normal','Once')
	item2_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Don't Drink Soda",'Normal','Once')
	item3_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Eat small portions","Normal","Once")
	item4_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Minimize starches and sugars","Normal","Once")
	item5_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Choose lean proteins","Normal","Once")
	item6_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"When having chicken,avoid eating the skin or eating it fried","Normal","Once")
	item7_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Eat more salmon","Normal","Once")
	item8_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Eat fresh fish","Normal","Once")
	item9_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Eat pieces of meat no larger than your fist","Normal","Once")
	item10_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Minimize foods that are white, like rice,potato","Normal","Once")
	item11_checklist_eating_healthy1 = add_listitem(checklist_eating_healthy1,"Eat vegetable with every meal","Normal","Once")
	
	checklist_eating_healthy2 = add_checklist(healthy_diet,doctor2)
	item1_checklist_eating_healthy2 = add_listitem(checklist_eating_healthy2 ,"Eat seven servings of fruits or vegetables","Normal","Once")
	item2_checklist_eating_healthy2 = add_listitem(checklist_eating_healthy2 ,"Compare the taste of an organic product to your usual purchase","Normal","Once")
	item3_checklist_eating_healthy2 = add_listitem(checklist_eating_healthy2 ,"Try a new vegetarian entree or recipe","Normal","Once")
	item4_checklist_eating_healthy2 = add_listitem(checklist_eating_healthy2 ,"Keep fresh olive oil near the stove","Normal","Once")
	item5_checklist_eating_healthy2 = add_listitem(checklist_eating_healthy2 ,"Take the salt of the dining table","Normal","Once")
	
	checklist_eating_healthy3 = add_checklist(healthy_diet,doctor3)
	item1_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Balance each meal with protein, complex carbs and healthy fats","Normal","Once")
	item2_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Balance: 15 % protein 55% carbs 30% fat","Normal","Once")
	item3_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Limit sugar and salt","Normal","Once")
	item4_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Cook with olive oil","Normal","Once")
	item5_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Bake, broil, sauté","Normal","Once")
	item6_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Avoid deep frying","Normal","Once")
	item7_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Fill half of your plate with fruits and vegetables","Normal","Once")
	item8_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Eat fresh foods","Normal","daily")
	item9_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Avoid processed foods","Normal","daily")
	item10_checklist_eating_healthy3 = add_listitem(checklist_eating_healthy3 ,"Eat breakfast","Normal","daily")
	
	checklist_losing_weight1 = add_checklist(losing_weight,doctor4)
	item1_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Early on, visit your primary care physician to check general health","Normal","Yearly")
	item2_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Drink half your weight in ounces of water","Normal","Daily")
	item3_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Consult a nutritionist if you're unsure of healthy food choices","Normal","Once")
	item4_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Eat on a regular basis (3 meals, 2 snacks) to avoid excessive hunger","Normal","Once")
	item5_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Focus on non-starch vegetables to fill up as needed","Normal","Once")
	item6_checklist_losing_weight1 = add_listitem(checklist_losing_weight1,"Enlist a counselor to work on non-food self soothing","Normal","Once")
	
	checklist_losing_weight2 = add_checklist(losing_weight,doctor5)
	item1_checklist_losing_weight2 = add_listitem(checklist_losing_weight2,"Evaluate your eating habits and choose a diet plan that you can follow","Normal","Once")
	item2_checklist_losing_weight2 = add_listitem(checklist_losing_weight2,"Eliminate Soda from your diet","Normal","Once")
	item3_checklist_losing_weight2 = add_listitem(checklist_losing_weight2,"Stick to a daily exercise plan,get a trainer of possible","Normal","Once")
	
	checklist_getting_fit1 = add_checklist(getting_fit,doctor1)
	item1_getting_fit1 = add_listitem(checklist_getting_fit1,"Make a promise you will improve your health and write it down","Normal","Once")
	item2_getting_fit1 = add_listitem(checklist_getting_fit1,"Exercise regularly","Normal","Once")
	item3_getting_fit1 = add_listitem(checklist_getting_fit1,"Walk or bike daily","Normal","Daily")
	item4_getting_fit1 = add_listitem(checklist_getting_fit1,"Avoid the elevator","Normal","Once")
	
	checklist_getting_fit2 = add_checklist(getting_fit,doctor2)
	item1_getting_fit2 = add_listitem(checklist_getting_fit2,"Walk, jog, cycle or swim","Normal","5x week")
	item2_getting_fit2 = add_listitem(checklist_getting_fit2,"eat diet rich in fruits, vegetables, whole grains","Normal","daily")
	item3_getting_fit2 = add_listitem(checklist_getting_fit2,"include lean protein (eggs, fish, chicken, lean beef) in diet","Normal","daily")
	item4_getting_fit2 = add_listitem(checklist_getting_fit2,"Choose good fats","Normal","daily")
	item5_getting_fit2 = add_listitem(checklist_getting_fit2,"get sufficient sleep","Normal","daily")
	item6_getting_fit2 = add_listitem(checklist_getting_fit2,"keep consistent sleep/wake times","Normal","daily")
	item7_getting_fit2 = add_listitem(checklist_getting_fit2,"eaet breakfast","Normal","daily")
	
	checklist_getting_fit3 = add_checklist(getting_fit,doctor3)
	item1_getting_fit3 = add_listitem(checklist_getting_fit3,"Start slow.Walk at a pace that allows you to talk.","Normal","daily")
	item2_getting_fit3 = add_listitem(checklist_getting_fit3,"Go slow.Advance your speed and distance when the walk feels too easy","Normal","daily")
	item3_getting_fit3 = add_listitem(checklist_getting_fit3,"Get physical exercise everyday, even for only 10 minutes","Normal","daily")
	item3_getting_fit3 = add_listitem(checklist_getting_fit3,"Add strength, balance, and stretching exercises to workout","Normal","every other day")
	
	checklist_getting_fit4 = add_checklist(getting_fit,doctor4)
	item1_getting_fit4 = add_listitem(checklist_getting_fit4,"walk, jog, cycle or swim","Normal","5x week")
	item2_getting_fit4 = add_listitem(checklist_getting_fit4,"eat diet rich in fruits, vegetables, whole grains","Normal","daily")
	item3_getting_fit4 = add_listitem(checklist_getting_fit4,"include lean protein (eggs, fish, chicken, lean beef) in diet","Normal","daily")
	item4_getting_fit4 = add_listitem(checklist_getting_fit4,"choose good fats(olive oil)","Normal","daily")
	item5_getting_fit4 = add_listitem(checklist_getting_fit4,"get sufficient sleep","Normal","daily")
	item6_getting_fit4 = add_listitem(checklist_getting_fit4,"keep consistent sleep/wake times","Normal","daily")
	item7_getting_fit4 = add_listitem(checklist_getting_fit4,"eat breakfast","Normal","daily")
	
	#add checklist sleeping better 
	checklist_sleeping_better1 = add_checklist(sleeping_better,doctor1)
	item1_sleeping_better1 = add_listitem(checklist_sleeping_better1,"Go to bed at the same time every day","Normal","daily")
	item2_sleeping_better1 = add_listitem(checklist_sleeping_better1,"Wake up the the same time every day","Normal","daily")
	item3_sleeping_better1 = add_listitem(checklist_sleeping_better1,"Don't drink alcohol before bedtime","Normal","daily")
	item4_sleeping_better1 = add_listitem(checklist_sleeping_better1,"Use your bed only for sleep(and sex)","Normal","Once")
	item5_sleeping_better1 = add_listitem(checklist_sleeping_better1,"Sleep with the TV/radio/computer off","Normal","Once")
	item6_sleeping_better1 = add_listitem(checklist_sleeping_better1,"if you can't sleep after 20 minutes, get out of bed","Normal","Once")
	
	checklist_sleeping_better2 = add_checklist(sleeping_better,doctor2)
	item1_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Create a cool,dark, and quite environment to sleep","Normal","Once")
	item2_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Try and keep the same time each night for sleep and awakening","Normal","Once")
	item3_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Eliminate caffeine 4-6 hours before bedtime","Normal","Once")
	item4_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Write down any recurring thoughts before bed to help clear your mind","Normal","Once")
	item5_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Wear loose and comfortable clothing","Normal","Once")
	item6_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Limit naps to 30 minutes or less","Normal","Once")
	item7_sleeping_better2 = add_listitem(checklist_sleeping_better2,"Use your bed for only sex and sleep","Normal","Once")
	
	#add checklist improving_heart_health
	checklist_improving_heart_health1 = add_checklist(improving_heart_health,doctor3)
	item1_improving_heart_health = add_listitem(checklist_improving_heart_health1,"Find an activity you enjoy, and do it daily for at least 20 minutes","Normal","Daily")
	item2_improving_heart_health = add_listitem(checklist_improving_heart_health1,"Intensify workouts by doing max intensity for 2 min, every 5-10 min","Normal","Once")
	
	checklist_improving_heart_health2 = add_checklist(improving_heart_health,doctor4)
	item1_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Maintain normal weight","Normal","Once")
	item2_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Walk, cycle, swim or jog","Normal","5x week")
	item3_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Limit salt and sugar intake","Normal","Once")
	item4_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Maintain dental health with brushing and flossing","Normal","Once")
	item5_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Eat a Mediterranean diet","Normal","Once")
 	item6_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Maintain normal blood pressure","Normal","once")
	item7_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Get sufficient rest","Normal","Once")
	item8_improving_heart_health2 = add_listitem(checklist_improving_heart_health2,"Pet your dog","Normal","daily")
	
	#add checklist quit smoking 
	checklist_quit_smoking1 = add_checklist(quit_smoking,doctor1)
	item1_quit_smoking1 = add_listitem(checklist_quit_smoking1,"Commit to quitting -- tell friends and family to stay accountable","Normal","Once")
	item2_quit_smoking1 = add_listitem(checklist_quit_smoking1,"Pick a date to stop and write it down","Normal","Once")
	item3_quit_smoking1 = add_listitem(checklist_quit_smoking1,"Explore quitting aids like the patch, gum, and pre scripting drugs","Normal","Once")
	item4_quit_smoking1 = add_listitem(checklist_quit_smoking1,"Seek support -- quitting can be hard","Normal","Once")
	
	checklist_quit_smoking2 = add_checklist(quit_smoking,doctor2)
	item1_quit_smoking2 = add_listitem(checklist_quit_smoking2,"Make your decision, then choose a buddy/supporter","Normal","Once")
	item2_quit_smoking2 = add_listitem(checklist_quit_smoking2,"Discuss your plan with your doctor","Normal","Once")
	item3_quit_smoking2 = add_listitem(checklist_quit_smoking2,"Choose a quit date that's meaningful too you","Normal","Once")
	item4_quit_smoking2 = add_listitem(checklist_quit_smoking2,"Cut out the source(where you buy the cigarettes, the money/credit)","Normal","Once")

	# add checklist imporving relation ship 
	checklist_improving_relation_ship1 = add_checklist(improving_relationships,doctor1)
	item1_improving_relationship1 = add_listitem(checklist_improving_relation_ship1,"Practice good communication","Normal","Once")
	item2_improving_relationship1 = add_listitem(checklist_improving_relation_ship1,"Get counselling of appropriate","Normal","Once")
	item3_improving_relationship1 = add_listitem(checklist_improving_relation_ship1,"Make time for each other","Normal","Once")

	checklist_improving_relation_ship2 = add_checklist(improving_relationships,doctor2)
	item1_improving_relationship2 = add_listitem(checklist_improving_relation_ship2,"Try to listen more than you speak","Normal","Once")
	item2_improving_relationship2 = add_listitem(checklist_improving_relation_ship2,"Try to respect one another","Normal","Once")
	item3_improving_relationship2 = add_listitem(checklist_improving_relation_ship2,"Spend time doing a satisfying activity","Normal","Once")

	# add checklsit healthy traveling 
	checklist_healthy_traveling1 = add_checklist(healthy_traveling,doctor2)
	item1_healthy_traveling1 = add_listitem(checklist_healthy_traveling1,"Drink bottle water or boil water from the tap","Normal","Once")
	item2_healthy_traveling1 = add_listitem(checklist_healthy_traveling1,"Avoid swallowing water when brushing your teeth","Normal","Once")
	item3_healthy_traveling1 = add_listitem(checklist_healthy_traveling1,"Take all required immunizations when travelling to a foreign country","Normal","Once")
	
	# add checklsit deal_emesis
	checklist_deal_emesis1 = add_checklist(deal_emesis,doctor2)
	item1_deal_emesis1 = add_listitem(checklist_deal_emesis1,"stick to clear liquids, like ice chips and popsicles","Normal","Once")
	item2_deal_emesis1= add_listitem(checklist_deal_emesis1,"Drink small amounts of fluids frequently","Normal","Once")
	item3_deal_emesis1 = add_listitem(checklist_deal_emesis1,"Avoid solids until you're able to go several hours without vomiting","Normal","Once")
	item4_deal_emesis1 = add_listitem(checklist_deal_emesis1,"Star with a very bland diet once you're able to eat","Normal","Once")

	# add abnormal_heart_rhythm
	checklist_abnormal_heart_rhythm1 = add_checklist(abnormal_heart_rhythm,doctor1)
	item1_abnormal_heart_rhythm1 = add_listitem(checklist_abnormal_heart_rhythm1,"Make healthy lifestyle choices","Normal","Once")
	item2_abnormal_heart_rhythm1 = add_listitem(checklist_abnormal_heart_rhythm1,"Stop smoking and avoid second-hand smoke","Normal","Once")
	item3_abnormal_heart_rhythm1 = add_listitem(checklist_abnormal_heart_rhythm1,"Avoid excessive amounts of caffeine and alcohol","Normal","Once")

	checklist_abnormal_heart_rhythm2 = add_checklist(abnormal_heart_rhythm,doctor5)
	item1_abnormal_heart_rhythm2 = add_listitem(checklist_abnormal_heart_rhythm2,"Work with your doctor to identify problem","Normal","Once")
	item2_abnormal_heart_rhythm2 = add_listitem(checklist_abnormal_heart_rhythm2,"Identify the risks and triggers for arrhythmia","Normal","Once")
	item3_abnormal_heart_rhythm2 = add_listitem(checklist_abnormal_heart_rhythm2,"Take prescribed medications without fail","Normal","Once")

	# add accidental_poisoning
	checklist_accidental_poisoning1 = add_checklist(accidental_poisoning,doctor2)
	item1_accidental_poisoning1 = add_listitem(checklist_accidental_poisoning1,"Call 911 and poison control immediately","Normal","Once")
	item2_accidental_poisoning1 = add_listitem(checklist_accidental_poisoning1,"Protect yourself from exposure if necessary","Normal","Once")
	item3_accidental_poisoning1 = add_listitem(checklist_accidental_poisoning1,"Gather and evidence possible about poisoning or exposure","Normal","Once")
	item4_accidental_poisoning1 = add_listitem(checklist_accidental_poisoning1,"Remember what and how much subtance the person ingested or inhaled","Normal","Once")
	item5_accidental_poisoning1 = add_listitem(checklist_accidental_poisoning1,"if anxious, quickly write down anything necessary for medical staff","Normal","Once")
	
	checklist_accidental_poisoning2 = add_checklist(accidental_poisoning,doctor3)
	item1_accidental_poisoning2 = add_listitem(checklist_accidental_poisoning2,"If patient is unstable or in significant distress, call 911","Normal","Once")
	item2_accidental_poisoning2 = add_listitem(checklist_accidental_poisoning2,"Call poison control, and have container of poison and hand for call","Normal","Once")
	item3_accidental_poisoning2 = add_listitem(checklist_accidental_poisoning2,"Follow direction from poison control","Normal","Once")
	item4_accidental_poisoning2 = add_listitem(checklist_accidental_poisoning2,"Keep all potential poisons out of reach of children","Normal","Once")
	
	#add manage acne 
	checklist_manage_acne1 = add_checklist(manage_acne,doctor4)
	item1_manage_acne1 = add_listitem(checklist_manage_acne1,"Use a gentle cleanser designed for acne-prone skin","Normal","1 Min, Daily for 2 years")
	item2_manage_acne1 = add_listitem(checklist_manage_acne1,"Use over-the-counter or prescription acne drugs as the doctor advises","Normal","Daily")
	item3_manage_acne1 = add_listitem(checklist_manage_acne1,"See the doctor to adjust medications and other treatments","Normal","3x Year")

	checklist_manage_acne2 = add_checklist(manage_acne,doctor5)
	item1_manage_acne2 = add_listitem(checklist_manage_acne2,"See a Doctor to prescribe a treatment plan based on your acne severity","Normal","Once")
	item2_manage_acne2 = add_listitem(checklist_manage_acne2,"Use your medications consistently","Normal","Daily")
	item3_manage_acne2 = add_listitem(checklist_manage_acne2,"Wash twice daily & after exercise, make-up removal, extra oily skin","Normal","2x a day")
	item4_manage_acne2 = add_listitem(checklist_manage_acne2,"Use mild, oil-free soaps, avoid ex foliating products, and don't scrub","Normal","Daily")
	item5_manage_acne2 = add_listitem(checklist_manage_acne2,"Wear sunblock. Several acne medications cause photosensitive","Normal","Daily")
	item6_manage_acne2 = add_listitem(checklist_manage_acne2,"Eat healthy & balanced diet. Avoid junk foods","Normal","3x day")
	item7_manage_acne2 = add_listitem(checklist_manage_acne2,"See a Doctor to prescribe a treatment plan based on your acne severity","Normal","Once")
	item8_manage_acne2 = add_listitem(checklist_manage_acne2,"Early intervention is key. See your doctor soon if treatment failing","Normal","Once")
	
	#add treating_acute_bronchitis
	checklist_treating_acute_bronchitis1 = add_checklist(treating_acute_bronchitis,doctor1)
	item1_treating_acute_bronchitis1 = add_listitem(checklist_treating_acute_bronchitis1,"Drink plenty of water","Normal","Daily")
	item2_treating_acute_bronchitis1 = add_listitem(checklist_treating_acute_bronchitis1,"Take ibuprofen for pain","Normal","Daily")
	
	checklist_treating_acute_bronchitis2 = add_checklist(treating_acute_bronchitis,doctor2)
	item1_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Quit smoking, if you're a smoker","Normal","Once")
	item2_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Drink plenty of water to loosen phlegm","Normal","every 4-6 hours")
	item3_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Use cough expectorants only if necessary","Normal","Once")
	item4_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Use cough suppressants only if necessary","Normal","Once")
	item5_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Drink warm fluids, which may ease daytime cough","Normal","Once")
	item6_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Complete antibiotics if prescribed by your doctor","Normal","Once")
	item7_treating_acute_bronchitis2 = add_listitem(checklist_treating_acute_bronchitis2,"Follow up with doctor if cough persists longer than 4 weeks","Normal","Once")

	#ADD CHECKLIST living_aids
	checklist_living_aids1 = add_checklist(living_aids,doctor1)
	item1_checklist_living_aids1 = add_listitem(checklist_living_aids1,"Choose your doctor carefully","Normal","Once")
	item2_checklist_living_aids1 = add_listitem(checklist_living_aids1,"Understand your disease in detail","Normal","Once")
	item3_checklist_living_aids1 = add_listitem(checklist_living_aids1,"Be compliant and adherent with your medications","Normal","Once")
	item4_checklist_living_aids1 = add_listitem(checklist_living_aids1,"Keep your appointments regularly","Normal","Once")
	
	#add manage_anger
	checklist_manage_anger1 = add_checklist(manage_anger, doctor2)
	item1_checklist_manage_anger1 = add_listitem(checklist_manage_anger1,"Be aware of internal and anxiety and count to 10","Normal","Once")
	item2_checklist_manage_anger1 = add_listitem(checklist_manage_anger1,"Identify the source of stress; that is 90% of the solution","Normal","Once")
	item3_checklist_manage_anger1 = add_listitem(checklist_manage_anger1,"Join a support group to help you cope","Normal","Once")
	
	checklist_manage_anger2 = add_checklist(manage_anger,doctor3)
	item1_checklist_manage_anger2 = add_listitem(checklist_manage_anger2,"Count to 10 when angry","Normal","Once")
	item2_checklist_manage_anger2 = add_listitem(checklist_manage_anger2,"Remove yourself from the situation","Normal","Once")
	item3_checklist_manage_anger2 = add_listitem(checklist_manage_anger2,"Talk it out","Normal","Once")
	item4_checklist_manage_anger2 = add_listitem(checklist_manage_anger2,"Get 8 hours sleep","Normal","Daily")
	item5_checklist_manage_anger2 = add_listitem(checklist_manage_anger2,"Avoid alcohol and drugs","Normal","Once")
	
	# add taking_antibio
	checklist_taking_antibio1 = add_checklist(taking_antibio,doctor4)
	item1_checklist_taking_antibio1 = add_listitem(checklist_taking_antibio1,"Follow directions on label","Normal","Once")
	item2_checklist_taking_antibio1 = add_listitem(checklist_taking_antibio1,"Take all doses as directed. Dont stop when you feel better.","Normal","Once")
	item3_checklist_taking_antibio1 = add_listitem(checklist_taking_antibio1,"Do not take someone else's antibiotic","Normal","Once")
	item4_checklist_taking_antibio1 = add_listitem(checklist_taking_antibio1,"Throw away any leftover antibiotics when you're done","Normal","Once")
	item5_checklist_taking_antibio1 = add_listitem(checklist_taking_antibio1,"Don't take leftover or expired antibiotics","Normal","Once")
	
	checklist_taking_antibio2 = add_checklist(taking_antibio,doctor5)
	item1_checklist_taking_antibio2 = add_listitem(checklist_taking_antibio2,"Take with food","Normal","Once")
	item2_checklist_taking_antibio2 = add_listitem(checklist_taking_antibio2,"Always finish the course whether you feel better early or not","Normal","Once")
	item3_checklist_taking_antibio2 = add_listitem(checklist_taking_antibio2,"Watch for abdominal pain and diarrhea call Dr if occurs ","Normal","Once")
	
	#add overcome_stress
	checklist_overcome_stress1 = add_checklist(overcome_stress,doctor1)
	item1_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"As your stress or anxiety level is rising, stop what you're doing","Normal","Once")
	item2_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"Rate level of distress you're feeling from 0(none) to 100(overload)","Normal","Once")
	item3_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"Ask yourself 'what bad thing am I expecting to happened?'","Normal","Once")
	item4_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"Slowly inhale through your nose and exhale through your mouth","Normal","Once")
	item5_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"While breathing, think to yourself 'I can handle feeling distress'","Normal","Once")
	item6_checklist_overcome_stress1 = add_listitem(checklist_overcome_stress1,"When you feel like stopping, congratulate yourself on your efforts","Normal","Once")

	#add overcome_fatigue
	checklist_overcome_fatigue1 = add_checklist(overcome_fatigue,doctor4)
	item1_checklist_overcome_fatigue1 = add_listitem(checklist_overcome_fatigue1,"et a full night's sleep","Normal","Daily")
	item2_checklist_overcome_fatigue1 = add_listitem(checklist_overcome_fatigue1,"See your doctor to investigating medical causes","Normal","Daily")
	item3_checklist_overcome_fatigue1 = add_listitem(checklist_overcome_fatigue1,"Set a regular bedtime","Normal","Daily")
	item4_checklist_overcome_fatigue1 = add_listitem(checklist_overcome_fatigue1,"Eat a healthy diet","Normal","Daily")

	#add treating_fever
	checklist_treating_fever1 = add_checklist(treating_fever,doctor5)
	item1_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"Don't panic! Most fever is uncomfortable, but harmless","Normal","Once")
	item2_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"Take the appropriate does of acetaminophen or ibuprofen","Normal","Once")
	item3_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"Try cool compresses -- they may be soothing","Normal","Once")
	item4_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"See doctor if your fever is higher than 102F for more than 2 days","Normal","Once")
	item5_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"See your doctor if your fevers is higher than 104F","Normal","Once")
	item6_checklist_treating_fever1 = add_listitem(checklist_treating_fever1,"See your doc for any fever associated with significant behaviour change","Normal","Once")
	
	checklist_treating_fever2 = add_checklist(treating_fever,doctor2)
	item1_checklist_treating_fever2 = add_listitem(checklist_treating_fever2,"Alternate acetaminophen and ibuprofen","Normal","every 3 hours")
	item2_checklist_treating_fever2 = add_listitem(checklist_treating_fever2,"Be sure to dose the fever reducers appropriately","Normal","Once")
	item3_checklist_treating_fever2 = add_listitem(checklist_treating_fever2,"Take tepid showers or baths to reduce fever, until just light shivers","Normal","Once")
	item4_checklist_treating_fever2 = add_listitem(checklist_treating_fever2,"Drink extra fluids to make up for loss","Normal","Once")
	item5_checklist_treating_fever2 = add_listitem(checklist_treating_fever2,"If your fever lasts more than three days, see your doctor","Normal","Once")
	
	#add caregiving for a spoouse 
	checklist_caregiving1 = add_checklist(caregiving,doctor1)
	item1_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Keep important information in a dedicated notebook","Normal","Once")
	item2_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Keep info like SS#, Medicare ID, insurance cards & doctor info handy","Normal","Once")
	item3_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Keep a list of allergies, medications, and medical conditions","Normal","Once")
	item4_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Know advanced directives and health care proxy numbers","Normal","Once")
	item5_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Safety-proof your home for someone with health challenges","Normal","Once")
	item6_checklist_caregiving1 = add_listitem(checklist_caregiving1,"Install handrails, and make sure the bathroom has grab bars","Normal","Once")
	
	#add miscarriage
	checklist_miscarriage1 = add_checklist(miscarriage,doctor2)
	item1_checklist_miscarriage1 = add_listitem(checklist_miscarriage1,"See your Doc to make suer you are medically OK","Normal","Once")
	item2_checklist_miscarriage1 = add_listitem(checklist_miscarriage1,"Keep perspective. 1 in 5 pregnancies end in a miscarriage","Normal","Daily")
	item3_checklist_miscarriage1 = add_listitem(checklist_miscarriage1,"Its probably not you fault. Making a human is complex","Normal","Daily")
	item4_checklist_miscarriage1 = add_listitem(checklist_miscarriage1,"Grieve. You've had a death in the family. It takes time to grieve","Normal","Daily")
	item5_checklist_miscarriage1 = add_listitem(checklist_miscarriage1,"Wait several months before you try again. Your body needs to recover","Normal","Monthly")

	#add healthy_pregnancy
	checklist_healthy_pregnancy1 = add_checklist(healthy_pregnancy,doctor1)
	item1_checklist_healthy_pregnancy1 = add_listitem(checklist_healthy_pregnancy1,"Don't smoke","Normal","Once")
	item2_checklist_healthy_pregnancy1 = add_listitem(checklist_healthy_pregnancy1,"Take a walk; walking promotes easier labor","Normal","Daily")
	item3_checklist_healthy_pregnancy1 = add_listitem(checklist_healthy_pregnancy1,"Take prenatal vitamins with folate to reduce birth defects","Normal","Daily")
	item4_checklist_healthy_pregnancy1 = add_listitem(checklist_healthy_pregnancy1,"Eat a healthy diet, including lots of fruit and dairy products","Normal","Daily")
	
	checklist_healthy_pregnancy2 = add_checklist(healthy_pregnancy,doctor4)
	item1_checklist_healthy_pregnancy2 = add_listitem(checklist_healthy_pregnancy2,"Eat smaller, more frequent meals and snacks","Normal","6x day")
	item2_checklist_healthy_pregnancy2 = add_listitem(checklist_healthy_pregnancy2,"Avoid lying down immediately after eating","Normal","Once")
	item3_checklist_healthy_pregnancy2 = add_listitem(checklist_healthy_pregnancy2,"Prevent nausea by avoiding fatty foods that are difficult to digest","Normal","Once")
	item4_checklist_healthy_pregnancy2 = add_listitem(checklist_healthy_pregnancy2,"Drink fluids between meals rather than with","Normal","Once")
	item5_checklist_healthy_pregnancy2 = add_listitem(checklist_healthy_pregnancy2,"Eat slowly to give your body time to tell you once you're full","Normal","Once")
	
	#add try_conceive
	checklist_try_conceive1 = add_checklist(try_conceive,doctor1)
	item1_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Don't smoke","Normal","Once")
	item2_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Take a folic acid supplement","Normal","Once")
	item3_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Talk to your doctor about medications/supplements that you are taking","Normal","Once")
	item4_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Predict ovulation","Normal","Once")
	item5_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Have sex near ovulation","Normal","Once")
	item6_checklist_try_conceive1 = add_listitem(checklist_try_conceive1,"Relax","Normal","Once")
	
	checklist_try_conceive2 = add_checklist(try_conceive,doctor2)
	item1_checklist_try_conceive2 = add_listitem(checklist_try_conceive2,"Realize that you are not alone. 1 in 5 pregnancies miscarry","Normal","Once")
	item2_checklist_try_conceive2 = add_listitem(checklist_try_conceive2,"Most likely it isn't your fault. Its not something you ate or smelled","Normal","Once")
	item3_checklist_try_conceive2 = add_listitem(checklist_try_conceive2,"Your are making a human. Its complicated and things go wrong.","Normal","Once")
	item4_checklist_try_conceive2 = add_listitem(checklist_try_conceive2,"You will need to grieve the loss. You are already bonded.","Normal","Once")
	item5_checklist_try_conceive2 = add_listitem(checklist_try_conceive2,"If you become depressed, see your doctor. Sometimes meds help","Normal","Once")

	#add breastfeeding
	checklist_breastfeeding1 = add_checklist(breastfeeding,doctor3)
	item1_checklist_breastfeeding1 = add_listitem(checklist_breastfeeding1,"Drink plenty of water","Normal","every 4 hours")
	item2_checklist_breastfeeding1 = add_listitem(checklist_breastfeeding1,"Rest","Normal","every 6 hours")
	item3_checklist_breastfeeding1 = add_listitem(checklist_breastfeeding1,"Join a breastfeeding support group","Normal","Once")
	item4_checklist_breastfeeding1 = add_listitem(checklist_breastfeeding1,"Eat healthy food","Normal","every 4 hours")
	
	checklist_breastfeeding2 = add_checklist(breastfeeding,doctor4)
	item1_checklist_breastfeeding2 = add_listitem(checklist_breastfeeding2,"Drink a lot of fluid - drink a cup of milk/water each time you nurse.","Normal","every 4 hours")
	item2_checklist_breastfeeding2 = add_listitem(checklist_breastfeeding2,"Make sure your baby has a good latch(open baby;s moth wide!)","Normal","every 4 hours")
	
	#add aging_graceful
	checklist_aging_graceful1 = add_checklist(aging_graceful,doctor1)
	item1_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Eat greens, beans, and whole grains daily.Avoid refined crabs.","Normal","Daily")
	item2_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Get regular aerobic exercise","Normal","5x week")
	item3_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Perform strength-training exercises","Normal","Daily")
	item4_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Do not smoke, drink alcohol, or take illicit drugs","Normal","Daily")
	item5_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Sleep at least 7 hours per night","Normal","Once every night")
	item6_checklist_aging_graceful1 = add_listitem(checklist_aging_graceful1,"Learn something new","Normal","Daily")
	
	checklist_aging_graceful2 = add_checklist(aging_graceful,doctor2)
	item1_checklist_aging_graceful2 = add_listitem(checklist_aging_graceful2,"Get some exercise by taking a walk","Normal","3x week")
	item2_checklist_aging_graceful2 = add_listitem(checklist_aging_graceful2,"Learn something new","Normal","Weekly")
	item2_checklist_aging_graceful2 = add_listitem(checklist_aging_graceful2,"Eat Vegetable/Fibers","Normal","3x week")
	
	#add understand_girl_purberty
	checklist_understand_girl_purberty1 = add_checklist(understand_girl_purberty,doctor1)
	item1_checklist_understand_girl_purberty1 = add_listitem(checklist_understand_girl_purberty1,"Read a book about puberty","Normal","Once")
	item2_checklist_understand_girl_purberty1 = add_listitem(checklist_understand_girl_purberty1,"Give your daughter a book about puberty","Normal","Once")
	item3_checklist_understand_girl_purberty1 = add_listitem(checklist_understand_girl_purberty1,"Buy pads and have them ready before your daughter gets her period","Normal","Once")
	item4_checklist_understand_girl_purberty1 = add_listitem(checklist_understand_girl_purberty1,"Have first talk about birth control and sexuality with your daughter","Normal","Once")
	
	checklist_understand_girl_purberty2 = add_checklist(understand_girl_purberty,doctor2)
	item1_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Don't dwell on your body changes","Normal","Once")
	item2_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Talk to your friends about concerns","Normal","Once")
	item3_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Talk to your doctor about any issues","Normal","Once")
	item4_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Don;t keep emotions inside you","Normal","Once")
	item5_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Treat others the way you want to be treated","Normal","Once")
	item6_checklist_understand_girl_purberty2 = add_listitem(checklist_understand_girl_purberty2,"Remember the feelings of the people around you","Normal","Once")
	
	#add topic 
	#altitude illness 
	
	altitude_illness = topic_add("Altitude illness","Altitude sickness—also known as acute mountain sickness (ams), altitude illness, hypobaropathy,'the altitude bends',or soroche—is a pathological effect of high altitude on humans, caused by acute exposure to low partial pressure of oxygen at high altitude. It commonly occurs above 2, 400 metres (8, 000 feet).")
	condition_add(altitude_illness)
	# add question for altitude illness 
	
	question1_altitude_illness = add_question(altitude_illness,"What are the most common symptoms of altitude illness?")
	answer1_question1_altitude_illness = add_answer(question1_altitude_illness,doctor1,"Symptoms of altitude sickness include headache, nausea, dizziness or unsteadiness, confusion, mental status changes, shortness of breath and coughing.When at altitude, descend immediately at least 1000 feet; if no improvement, descend another 1000 feet. Symptoms of hape and hace (high altitude pulmonary edema and high altitude cerebral edema) require immediate air evacuation.")
	answer2_question1_altitude_illness = add_answer(question1_altitude_illness,doctor3,"The earliest--if you are paying attention (and many, sadly, do not)--headache, loss of appetite, nausea, dizziness and insomnia.These can occur as low as 6500 feet, especially if you are active. Slowing down, letting yourself acclimate, or sleeping at a lower altitude are best. Taking diamox speeds your body's acclimatization. If symptoms advance-to those described above--get down further fast!")
	
	question2_altitude_illness = add_question(altitude_illness,"How can I treat altitude illness?")
	answer1_question2_altitude_illness = add_answer(question2_altitude_illness,doctor2,"The best treatment for altitude illness or altitude sickness is to decrease one's elevation by at least 1000 ft (quickly and safely.) if symptoms do not improve, one needs to descend another 1000 ft. If one has symptoms of hace (high altitude cerebral edema) or hape (high altitude pulmonary edema) contact search and rescue and arrange for emergent air evacuation")
	answer2_question2_altitude_illness = add_answer(question2_altitude_illness,doctor3,"High altitude illness is a serious issue and I am not sure i understand what you mean by altitude illness.The treatment for high altitude sickness is evacuation to a lower altitude, diuretic and oxygen.")
	
	question3_altitude_illness = add_question(altitude_illness,"Is there a cure for altitude illness?")
	answer1_question3_altitude_illness = add_answer(question3_altitude_illness,doctor5,"The immediate treatment and cure for altitude illness is generally returning to a lower altitude, hydration and oxygen.Should this progress to more serious things like acute mountain sickness, then hyperbaric field-treatment and immediate evacuation to the hospital for treatment with diuretics and steroids to prevent brain swelling is needed.")
	
	question4_altitude_illness = add_question(altitude_illness,"My mom gets altitude illness, so am I likely to get it later?")
	answer1_question4_altitude_illness = add_answer(question4_altitude_illness,doctor3,"Actually there has long been belief in a familial ink in the various forms of altitude illness--lung and brain edema, and a condition called chronic mountain sickness--seen in some living at high altitude.Scientists at ucsd located 2 genes: anp32d ; senp1 in their mapping study. Doesn't mean you will have altitude sickness like mom--many factors involved--but genetics also at play.")
	
	#medication 
	acetazolamide = topic_add_sub(altitude_illness,"Acetazolamide","Acetazolamide is a carbonic anhydrase inhibitor which is a kind of water pill or diuretic (heart failure drug, cardiovascular drug).")
	medication_add(acetazolamide)
	
	
	dexamethasone = topic_add_sub(altitude_illness,"Dexamethasone","Dexamethasone is a type of steroid medication. It has anti-inflammatory and immunosuppressant effects. It is 25 times more potent than cortisol in its glucocorticoid effect, while having minimal mineralocorticoid effect.")
	medication_add(dexamethasone)
	
	
	methazolamide = topic_add_sub(altitude_illness,"Methazolamide","Methazolamide (Neptazane) is a carbonic anhydrase inhibitor.")
	medication_add(methazolamide)
	
	
	nifedipine = topic_add_sub(altitude_illness,"Nifedipine","This is a blood pressure medication in the class of calcium channel blockers which results in lower blood pressure by relaxing blood vessels through blocking calcium mediated constriction. This certain CCB does not typically affect the heart rate as Diltiazem or verapamil can.")
	medication_add(nifedipine)
	
	
	anti_nausea_drug = topic_add_sub(altitude_illness,'Anti nausea drug','Nausea and vomiting agents are a kind of gastroenterology drug.')
	medication_add(anti_nausea_drug)
	
	
	hyperbaric_oxygen_therapy = topic_add_sub(altitude_illness,"Hyperbaric oxygen therapy","Hyperbaric oxygen therapy (hbot) is, by definition, the administration of oxygen at greater than atmospheric pressure. There are many indications for this type of treatment: radiation injuries, wounds related to diabetes or poor circulation, and others. Hbot is delivered in 1 of 2 ways: a monochamber (1 patient at a time) or a multichamber (more than 1 patient). The efficacy is the same.")
	
	
	oxygen_supplementation = topic_add_sub(altitude_illness,"Oxygen supplementation","Oxygen can be given by a mask worn over the face or a tube below the nose. This helps deliver more oxygen to people in circumstances when their natural oxygen levels are low.")
	
	#symptoom
	respiratory_disorders = topic_add_sub(altitude_illness,"Respiratory disorder","Pathological conditions that affect the respiratory system, to include upper respiratory tract, trachea, bronchi, bronchioles, alveoli, pleura & pleural cavity, as well as the nerves & muscles of breathing. They can range from mild such as the flu, to serious such as lung cancer.")
	condition_add(respiratory_disorders)
	
	
	vomitting = topic_add_sub(altitude_illness,"Vomiting","Nausea is the sensation of having an urge to vomit. Vomiting is forcing the contents of the stomach up through the esophagus and out of the mouth.")
	symptom_add(vomitting)
	
	cough = topic_add_sub(altitude_illness,"Cough","Coughing is an important way to keep your throat and airways clear. However, excessive coughing may mean you have an underlying disease or disorder. Some coughs are dry, while others are considered productive. A productive cough is one that brings up mucus.")
	symptom_add(cough)
	
	
	fever = topic_add_sub(altitude_illness,"fever","Fever is the temporary increase in the body's temperature in response to some disease or illness. A child has a fever when the temperature is at or above one of these levels: * 100.4")
	symptom_add(fever)
	
	
	nausea = topic_add_sub(altitude_illness,"nausea","Nausea is the sensation of having an urge to vomit.")
	symptom_add(nausea)
	
	
	fatigue = topic_add_sub(altitude_illness,"Fatigue","Fatigue (also called exhaustion, tiredness, languidness, languor, lassitude, and listlessness) is a subjective feeling of tiredness which is distinct from weakness, and has a gradual onset. Unlike weakness, fatigue can be alleviated by periods of rest. Fatigue can have physical or mental causes.")
	symptom_add(fatigue)
	
	
	balance_problems = topic_add_sub(altitude_illness,"balance_problems","Balance problems is a symptom in which a person has trouble staying in a steady position when sitting, standing, walking, running, etc.")
	symptom_add(balance_problems)
	
	
	headache = topic_add_sub(altitude_illness,"Headache","Also called cephalalgia, is pain anywhere in the region of the head or neck, & can be a symptom of a number of conditions affecting those areas. It originates from pain-sensitive structures such as cranium, muscles, nerves, vessels, subcutaneous tissues, eyes, ears, sinuses & mucous membranes. It is non-specific symptom & can be primary such as tension ha, or secondary such as organic causes.")
	symptom_add(headache)
	
	
	confusion = topic_add_sub(altitude_illness,"Confusion","The state of unclear thinking. May be accompanies by poor memory and disorientation")
	symptom_add(confusion)
	
	
	difficulty_sleeping = topic_add_sub(altitude_illness,"Difficulty sleeping","Many women complain that they have trouble sleeping when they are pregnant. Try not to eat just before bedtime. Consider taking a warm bath at bedtime to help you relax. As your abdomen gets bigger, you may want to lie on your side with a pillow under your abdomen and a pillow between your legs for comfort.")
	symptom_add(difficulty_sleeping)
	
	
	dizziness = topic_add_sub(altitude_illness,"Dizziness","Dizziness is light-headedness, feeling like you might faint, being unsteady, loss of balance, or vertigo (a feeling that you or the room is spinning or moving).")
	symptom_add(dizziness)
	
	#procedure add 
	xray_chest = topic_add_sub(altitude_illness,"Xray of chest","A chest x-ray is the basic radiographic study for evaluation of the heart and lungs. It usually consists of 2 views: postero-anterior and lateral. The image is now usually acquired digitally with the sensor placed against the front of the chest for the pa view and on the left side of the chest for the lateral view. Pneumonia, heart enlargement, CHF and many other conditions may be assessed.")
	procedure_add(xray_chest)
	
	
	eeg = topic_add_sub(altitude_illness,"Electrocardiogram(EEG)","Electrocardiogram (ecg, ekg) is a print-out of the electrical forces detected by electrodes on the chest wall, as electricity travels through the heart with each heart beat. The electrodes are placed in different positions, and each position 'sees' the electrical activity of the heart from its own vantage point. Abnormalities in signal detected at chest surface can indicate underlying disease.")
	procedure_add(eeg)
	
	
	ct_of_head = topic_add_sub(altitude_illness,"CT of head","Computed tomography (CT) of the head or Computed Axial Tomography (CAT) scanning uses a series of x-rays of the head taken from many different directions.Typically used for quickly viewing brain injuries, CT scanning uses a computer program that performs a numerical integral calculation (the inverse Radon transform) on the measured x-ray series to estimate how much of an x-ray beam is absorbed in a small volume of the brain. Typically the information is presented as a series of cross sections of the brain.")
	procedure_add(ct_of_head)
	
	
	mr_head=topic_add_sub(altitude_illness,"MR of head","A head MRI (magnetic resonance imaging) scan of the head is a imaging test that uses powerful magnets and radio waves to create pictures of the brain and surrounding nerve tissues.")
	procedure_add(mr_head)
	
	
	lumbar_puncture = topic_add_sub(altitude_illness,"Lumbar puncture","To test for meningitis or multiple sclerosis or a variety of problems, a small needle is inserted into the lumbosacral cistern to obtain spinal fluid for testing and perhaps diagnostic confirmation.")
	procedure_add(lumbar_puncture)
	
	
	wbc_count = topic_add_sub(altitude_illness,"WBC count","White blood cell count. That is, the number of WBC per microlitre of blood. It includes the common types of cells such as neutophils (granulocytes), lymhpocytes, monocytes, and the less common eosinophils and basophils.")
	procedure_add(wbc_count)
	
	
	arterial_blood_gas = topic_add_sub(altitude_illness,"Arterial blood gas","It's a blood test where blood is drawn from your artery (and not the vein where it's usually taken from). It is done to evaluate the amount of oxygen, carbon dioxide, acid and several other parameters in the blood.")
	procedure_add(arterial_blood_gas)
	
	
	echocardiogram = topic_add_sub(altitude_illness,"Echocardiogram","Echo refers to reflections of sound waves, typically 0.5-10mhz, sent through a body structure, all variants of water density. Cardio refers to heart. Gram refers to a picture or graphical representation of the data. A form of us, these help see certain aspects of our hearts behavior/function, real-time in motion picture video. Quality & usefulness varies widely as a function of situation/reader.")
	procedure_add(echocardiogram)
	
	#add new topic fever 
	fever = fever 
	#add_question 
	question1_fever = add_question(fever,"What could cause fevers?")
	answer1_question1_fever = add_answer(question1_fever,doctor5,"Most common cause is infections.")
	
	question2_fever = add_question(fever,"I am sweating at night but my body temperature is low. Does this mean fever? I'm concerned as i recently started tysabri")
	answer1_question2_fever = add_answer(question2_fever,doctor1,"No.But it could be a response to the tysabri.")
	
	question3_fever = add_question(fever,"My 3 yo son had congestion and fever. The fever only lasted a few hours. Now he has cough. Why was fever so short? Does cough mean it's almost over?")
	answer1_question3_fever = add_answer(question3_fever,doctor3,"Fever is triggered by immune response to infection.It's features (duration, intensity, etc) vary based on cause & individual immune responses. Viral upper respiratory infections are common at this age & can cause cough; usual course is 2 wks. However complications (pneumonia, etc) can occur; children do not complain; cues to worsening are missed. See doctor now for correct diagnosis & treatment.")	
	anwwer2_question3_fever = add_answer(question3_fever,doctor4,"infections are usually viral, of short duration and self limiting.For the first several days and up to 1 week - over the counter analgesics and fever reducing medications like Children's Motrin or Tylenol should be sufficient to control any symptoms. If these persist however after a week then it is reasonable to see your local family doctor or pediatrician for guidance.")
	#add medication 
	acetaminophen = topic_add_sub(fever,"Acetaminophen","Acetaminophen (tylenol) is a non-steroidal anti-inflammatory which is a kind of pain medication.")
	medication_add(acetaminophen)
	
	ibuprofen = topic_add_sub(fever,"Ibuprofen","Ibuprofen is a nonsteroidal anti-inflammatory drug (nsaid). It works by reducing hormones that cause inflammation and pain in the body. Ibuprofen is used to reduce fever and treat pain or inflammation caused by many conditions such as headache, toothache, back pain, arthritis, menstrual cramps, or minor injury.")
	medication_add(ibuprofen)
	
	aspirin = topic_add_sub(fever,"Aspirin","Aspirin is a non-steroidal anti-inflammatory which is a kind of pain medication.")
	medication_add(aspirin)
	
	naproxen = topic_add_sub(fever,"Naproxen","Naproxen is a non-steroidal anti-inflammatory drug. It inhibits cyclooxygenase thus reducing prostaglandin and thromboxane synthesis.")
	medication_add(naproxen)
	
	choline_magnesium_salicylate = topic_add_sub(fever,"Choline-magnesium-salicylate","Choline magnesium salicylate is a non-tricyclic which is a kind of serotonin-norepinephrine reuptake inhibiting drug (atypical anti-psychotic drug, drug for psychosis).")
	medication_add(choline_magnesium_salicylate)
	
	acne_rosacea = topic_add_sub(fever,"Acne rosacea","Acne rosacea is also known as Rosacea. Acne rosacea is a skin condition that can affect the adult face, and includes redness, swelling, and acne-like bumps.")
	medication_add(acne_rosacea)
	
	#add symptom 
	fatigue = topic_add_sub(fever,"Fatigue","Fatigue (also called exhaustion, tiredness, languidness, languor, lassitude, and listlessness) is a subjective feeling of tiredness which is distinct from weakness, and has a gradual onset. Unlike weakness, fatigue can be alleviated by periods of rest. Fatigue can have physical or mental causes.")
	
	confusion = topic_add_sub(fever,"Confusion","The state of unclear thinking. May be accompanies by poor memory and disorientation")

	muscle_pain = topic_add_sub(fever,"Muscle pain","Muscle pain is a symptom where a person has acute or chronic pain in one or more muscle groups, that can be due to a variety of causes including overuse and injury.")
	symptom_add(muscle_pain)
	
	headache = topic_add_sub(fever,"Headache","Also called cephalalgia, is pain anywhere in the region of the head or neck, & can be a symptom of a number of conditions affecting those areas. It originates from pain-sensitive structures such as cranium, muscles, nerves, vessels, subcutaneous tissues, eyes, ears, sinuses & mucous membranes. It is non-specific symptom & can be primary such as tension ha, or secondary such as organic causes.")

	chills = topic_add_sub(fever,"Chills","Chills may occur at the beginning of an infection and are usually associated with a fever. Chills are caused by rapid muscle contraction and relaxation, and are the body's way of generating heat when it feels that it is cold. Chills often predict the coming of a fever, or an increase in the body's core temperature.")
	symptom_add(chills)
	
	increased_sweating =topic_add_sub(fever,"Increased sweating","Increased sweating is a clinical finding in which a person experiences more sweating than he or most people typically do.")
	symptom_add(increased_sweating)
	
	night_terrors = topic_add_sub(fever,"Night terrors","Night terrors is a sleep condition that most often occurs in kids 3 to 12 years of age. Kids will often wake up suddenly terrified, screaming, and exhibiting signs of fight or flight such as rapid heart beat and sweating. Night terrors are different than nightmares or bad dreams in that night terrors are not dreams (which by definition occur in REM sleep) and kids will not remember them the next day.")
	symptom_add(night_terrors)
	
	hallucination = topic_add_sub(fever,"Hallucination","Hallucinations involve sensing things while awake that appear to be real, but instead have been created by the mind.")
	symptom_add(hallucination)
	
	dehydration = topic_add_sub(fever,"Dehydration","In physiology and medicine, dehydration (hypohydration) is the excessive loss of body water, with an accompanying disruption of metabolic processes.")
	symptom_add(dehydration)
	
	loss_of_appetite = topic_add_sub(fever,"Loss of appetite","Loss of appetite is a symptom in which a person loses some desire to eat or drink foods, and has less appetite than normal for somebody of his age and size. Many illnesses, physical and psychological, can cause a loss of appetite.")
	symptom_add(loss_of_appetite)
	
	#add_topic acute_sinusitis 
	acute_sinusitis = topic_add("Acute sinusitis","Acute sinusitis is an infection of the nose and the sinus airways behind the nose and inside the cheekbones. Most often the infection is caused by bacteria.")
	question1_acute_sinusitis = add_question(acute_sinusitis,"What is acute sinusitis?")
	answer1_question_acute_sinusitis = add_answer(question1_acute_sinusitis,doctor2,"Acute sinusitis is inflammation of the cavities around your nasal passages with associated mucus drainage, which makes it difficult for you to breathe through your nose.It may cause headache, pain around your eyes and cheeks. It’s typically due to a bacterial infection, but could be due to allergies, viral or fungal infections. Acute sinusitis lasts up to 4wks (subacute 4-12wks & chronic>12wks).")
	
	#add medication 
	amoxicillin_and_clavulanate = topic_add_sub(acute_sinusitis,"Amoxicillin and Clavulanate","Is a fixed combination of the pencillin class medication Amoxicillin with a compound that inhibits bacterial betalactamase expanding the activity of the amoxicillin.")
	medication_add(amoxicillin_and_clavulanate)
	
	cefdinir = topic_add_sub(acute_sinusitis,"Cefdinir","Cefdinir is a third generation cephalosporin which is a kind of cephalosporin type drug (anti-bacterial drug, antibiotic and antimicrobial).")
	medication_add(cefdinir)
	
	levofloxacin = topic_add_sub(acute_sinusitis,"Levofloxacin","Levofloxacin (trade names Levaquin (US), Tavanic (EU), and others) is a broad-spectrum antibiotic of the fluoroquinolone drug class and the levo isomer of its predecessor ofloxacin.")
	medication_add(levofloxacin)
	
	clarithromycin = topic_add_sub(acute_sinusitis,"Clarithromycin","Treats and prevents infections. Also used in combination with other medicines to treat duodenal ulcers caused by h. Pylori. This medicine is a macrolide antibiotic.")
	medication_add(clarithromycin)
	
	cefprozil = topic_add_sub(acute_sinusitis,"Cefprozil","Cefprozil is a second generation cephalosporin which is a kind of cephalosporin type drug (anti-bacterial drug, antibiotic and antimicrobial).")
	medication_add(cefprozil)
	
	#add symptom 
	cough = topic_add_sub(acute_sinusitis,"Cough","Coughing is an important way to keep your throat and airways clear. However, excessive coughing may mean you have an underlying disease or disorder. Some coughs are dry, while others are considered productive. A productive cough is one that brings up mucus.")
	
	sore_throat = topic_add_sub(acute_sinusitis,"Sore-throat","A sore throat is discomfort, pain, or scratchiness in the throat. A sore throat often makes it painful to swallow.")
	symptom_add(sore_throat)
	
	thick_mucus_drainage_from_nose = topic_add_sub(acute_sinusitis,"Thick mucus drainage from nose","Thick mucous drainage from the nose is a symptom in which the mucous coming out of the nose is thicker than clear mucous, and may also be yellowish or greenish in color. This may mean that there is a nasal or sinus bacterial infection.")
	symptom_add(thick_mucus_drainage_from_nose)
	
	dental_pain = topic_add_sub(acute_sinusitis,"Dental pain","Dental pain is a symptom where one has pain in his teeth or gums, sometimes with sensitivity to cold or hot temperatures, sour foods, etc.")
	symptom_add(dental_pain)
	
	headache = topic_add_sub(acute_sinusitis,"Headache","Also called cephalalgia, is pain anywhere in the region of the head or neck, & can be a symptom of a number of conditions affecting those areas. It originates from pain-sensitive structures such as cranium, muscles, nerves, vessels, subcutaneous tissues, eyes, ears, sinuses & mucous membranes. It is non-specific symptom & can be primary such as tension ha, or secondary such as organic causes.")
	
	fever = topic_add_sub(acute_sinusitis,"fever","Fever is the temporary increase in the body's temperature in response to some disease or illness. A child has a fever when the temperature is at or above one of these levels: * 100.4")
	
	nasal_drainage = topic_add_sub(acute_sinusitis,"Nasal drainage","Nasal discharge is common, but rarely serious. Drainage from swollen or infected sinuses may be thick or discolored.")
	symptom_add(nasal_drainage)
	
	congestion = topic_add_sub(acute_sinusitis,"Congestion","Congestion refers to any situation of 'backup of fluid.' Congestion may refer to the sinuses being backed up with mucus, while pulmonary congestion refers to a backup of fluid into the lungs due to problems with blood flow.")
	symptom_add(congestion)
	
	facial_pain = topic_add_sub(acute_sinusitis,"Facial pain","Facial pain is a clinical finding in which there is pain in the area of the face. This is often due to trauma, infections, or nerve problems.")
	symptom_add(facial_pain)
	
	blocked_nose = topic_add_sub(acute_sinusitis,"Blocked nose","A blocked nose is the sensation caused by a nasal passage congested with mucus, which can occur during a cold or with allergies.")
	symptom_add(blocked_nose)
	
	# add procedure 
	transillumination = topic_add_sub(acute_sinusitis,"Transillumination","Transillumination literally means line shining through. This principle may be used to diagnose maxillary sinusitis as the light will be blocked by the sinus infection and will not glow in the hard palate. Indeed, this procedure should be done in the dark. Transillumination is also used in diagnosing hydrocephalus and in histopathology labs.")
	procedure_add(transillumination)
	
	xray_of_sinuses = topic_add_sub(acute_sinusitis,"Xray of sinuses","A sinus X-ray uses radiation to form a picture of your sinuses.")
	procedure_add(xray_of_sinuses)
	
	ct_of_head = topic_add_sub(altitude_illness,"CT of head","Computed tomography (CT) of the head or Computed Axial Tomography (CAT) scanning uses a series of x-rays of the head taken from many different directions.Typically used for quickly viewing brain injuries, CT scanning uses a computer program that performs a numerical integral calculation (the inverse Radon transform) on the measured x-ray series to estimate how much of an x-ray beam is absorbed in a small volume of the brain. Typically the information is presented as a series of cross sections of the brain.")
	
	
	nasal_endoscopy = topic_add_sub(acute_sinusitis,"Nasal endoscopy","Nasal endoscopy is performed for an in depth examination of the nasal cavity. It is performed when an endoscope, or a sort of telescope whether flexible or rigid, is placed into the nose for the exam. Most often performed by an otolaryngologist.")
	procedure_add(nasal_endoscopy)
	
	allergy_tests = topic_add_sub(acute_sinusitis,"Allergy tests","Allergies can be identified by allergy tests. The best allergy test is a skin test. It is safe and reliable. The next best allergy test is a blood test - less reliable than skin tests but also safe. If we are looking into food allergy then a challenge test is very reliable but it can be risky.")
	procedure_add(allergy_tests)
	
	sinus_culture = topic_add_sub(acute_sinusitis,"Sinus culture","Blood tests may be ordered to identify underlying conditions such as cystic fibrosis, allergies or viral/bacterial infections. Mucus samples may also be obtained to identify underlying conditions.")
	procedure_add(sinus_culture)
	
	bipolar_affective_disorder = topic_add_sub(acute_sinusitis,"Bipolar affective diorder","Is a mood disorder characterized by swings from highs (mania or hypo mania) to lows (depression).")
	procedure_add(bipolar_affective_disorder)
	
	#add animal bite topic 
	
	animal_bite = topic_add("Animal bite","Animal bites is an injury in which a person's skin is damaged and usually cut open by the sharp teeth of an animal. Bites can lead to infections, usually bacterial infections. Rabies is quite rare in the U.S. (just 1 or 2 cases per year) thanks to animal control programs and vaccines for both animals and humans.")
	condition_add(animal_bite)
	#add question 
	question1_animal_bite = add_question(animal_bite,"What are the tests for animal bite?")
	answer1_question1_animal_bite = add_answer(question1_animal_bite,doctor4,"Well thats a problem you are placed in antibiotics if the site gets infected it can be cultured if the animal is wild you may need rabies shots you must seek out medical care for this asap.")
	anwer2_question1_animal_bite = add_answer(question1_animal_bite,doctor5,"Animal can be tested (brain) for rabies.Wound can be tested for other bacteria from, eg, cat bite.")
	
	#add symptom 
	fever = topic_add_sub(animal_bite,"fever","Fever is the temporary increase in the body's temperature in response to some disease or illness. A child has a fever when the temperature is at or above one of these levels: * 100.4")
	nausea = topic_add_sub(animal_bite,"nausea","Nausea is the sensation of having an urge to vomit.")
	chills = topic_add_sub(animal_bite,"Chills","Chills may occur at the beginning of an infection and are usually associated with a fever. Chills are caused by rapid muscle contraction and relaxation, and are the body's way of generating heat when it feels that it is cold. Chills often predict the coming of a fever, or an increase in the body's core temperature.")
	
	blistering = topic_add_sub(animal_bite,"Blistering","Blistering is a bubble of skin filled with fluid. They can occur to excessive rubbing (as with a new pair of shoes), or from burns.")
	symptom_add(blistering)
	
	joint_pain = topic_add_sub(animal_bite,"Joint pain","Joint pain is a clinical finding in which a joint (where two bones meet) is painful to move. This can occur with arthritis, crystal build up in joints, immune conditions, and infections.")
	symptom_add(joint_pain)
	
	skin_rash = topic_add_sub(animal_bite,"Skin rash","Skin rash is a symptom in which a person has changes on part or all of his skin, such as color changes, bumps, blisters, oozing, peeling, itching, bug bites, etc.")
	symptom_add(skin_rash)
	
	#add medication 
	amoxicillin_and_clavulanate = topic_add_sub(animal_bite,"Amoxicillin and clavulanate","Is a fixed combination of the pencillin class medication Amoxicillin with a compound that inhibits bacterial betalactamase expanding the activity of the amoxicillin")
	medication_add(amoxicillin_and_clavulanate)
	clindamycin = topic_add_sub(animal_bite,"Clindamycin","Part of the lincoside family . It has good gram positive an anaerobic coverage, but its association with the development of clostridium difficile infection has limited its use. It is used in certain drug allergy situations where staph, strep, pneumococcal, and anaerobic organisms. Its use in MRSA infections is spotty. It is a bacteriostatic drug that works on stopping protein synthesis")
	medication_add(clindamycin)
	
	# add topic common cold 
	common_cold = topic_add("Common cold","Viral upper respiratory tract infection, or URI, is a condition where there is a viral infection of the nose or throat, causing redness and inflammation, runny nose, and mild cough.")
	question1_common_cold = add_question(common_cold,"How do you diagnose common cold?")
	answer1_question1 = add_answer(question1_common_cold,doctor1,"Your doctor will make the diagnosis of a common cold based on your signs and symptoms by performing a history taking and a physical exam. The common cold generally involves a runny nose, nasal congestion, and sneezing.You may also have a sore throat, cough, or headache.")
	answer2_question1 = add_answer(question1_common_cold,doctor2,"It is diagnosed by the common symptoms of sore throat, runny or congested nose and in 30% of cases dry cough.")
	condition_add(common_cold)
	# add procedure 
	watchful_waiting = topic_add_sub(common_cold,"Watchful waiting","Watchful waiting, also known as expectant management, involves weighing the risks of treating an injury or illness against not treating it. Doctors will also consider the severity of symptoms the patient is having when deciding whether to 'watch and wait' or start treatment.")
	procedure_add(watchful_waiting)
	
	honey = topic_add_sub(common_cold,"Honey","Medicinal honey can serve as an antimicrobial when applied to wounds.")
	procedure_add(honey)
	
	bathroom_steam = topic_add_sub(common_cold,"Bathroom steam","Sometimes something as simple as turning the shower on hot, closing the bathroom door, and breathing the moist air can bring relief to a croupy cough. (Be careful to keep the hot water off the skin.)")
	procedure_add(bathroom_steam)
	
	# add topic Astigmatism
	astigmatism = topic_add("Astigmatism","Astigmatism is an eye condition that causes blurry vision because the eye is unable to focus light to a point and thus unable to produce a sharp image on the retina.")
	question1_astigmatism = add_question(astigmatism,"What is astigmatism?")
	answer1_question1 = add_answer(question1_astigmatism,doctor3,"Refractive errors require either plus (farsighted) or minus (nearsighted) glasses + an extra amount if the eye is oval in shape (astigmatism).These are called refractive errors and can be corrected with glasses or contacts. The list of other eye problems is long and these are usually unrelated to astigmatism.")
	answer2_question1 = add_answer(question1_astigmatism,doctor4,"Myopia (or nearsightedness), hyperopa (or farsightedness), and astigmatism all can cause refractive error. Refractive error is what causes a patient to require glasses or contact lenses to see better. Astigmatism is typically when the cornea is shaped more like a football than a basketball. Glasses, contact, and LASIK can fix this problem.")
	
	question2_astigmatism = add_question(astigmatism,"How to tell if I have astigmatism?")
	answer1_question2 = add_answer(question2_astigmatism,doctor2,"Most people have astigmatism which is when the front of the eye is not a perfect sphere.With significant astigmatism, your uncorrected (without glasses or contacts) vision is blurred. So if you don't have blurred vision, you don't have significant astigmatism. If you do have blurred vision, your eye doctor can tell you if it is due astigmatism or another cause.")
	
	#add medication 
	refractive_surgery = topic_add_sub(astigmatism,"Refractive surgery","LASIK is eye surgery that permanently changes the shape of the cornea (the clear covering on the front of the eye) in order to improve vision and reduce a person's dependency on glasses or contact lenses.")
	medication_add(refractive_surgery)
	# add topic 
	eye_disorders = topic_add_sub(astigmatism,"Eye disorders","Eye disorders are clinical conditions that affect the eyes and can cause vision loss, eye pain, or trouble with eye motion.")
	condition_add(eye_disorders)
	
	refractive_error = topic_add_sub(astigmatism,"Refractive error","Refractive error is an eye condition where there is a problem in focusing when viewing objects. Nearsightedness and farsightedness are due to refractive errors.")
	condition_add(refractive_error)
	
	# add symptom 
	farsightedness = topic_add_sub(astigmatism,"Farsightedness","Farsightedness (hyperopia) is a condition in which a person can see far away objects clearly, but close up objects are not clear. Farsightedness may cause eye strain and headaches, but can be corrected with glasses, contact lenses, or laser surgery.")
	symptom_add(farsightedness)
	
	nearsightedness = topic_add_sub(astigmatism,"Nearsightedness","Nearsightedness is a symptom where a person has trouble seeing clearing faraway objects.")
	symptom_add(nearsightedness)
	
	blurry_vision = topic_add_sub(astigmatism,"Blurry vision","Blurred vision is an ocular symptom.Blurred vision may be a systemic sign of local anaesthetic toxicity")
	symptom_add(blurry_vision)
	
	#add procedure 
	visual_acuity = topic_add_sub(astigmatism,"Visual acuity","Visual acuity is the measure of the sharpness of vision. It is the most important measurement of eye function. In the us, the antiquated snellen visual acuity measurement is most often used. This is the '20/20' thing you have no doubt heard of.")
	procedure_add(visual_acuity)
	
	#add topic anal fissure
	anal_fissure = topic_add("Anal fissure","Anal fissure is a condition where there is a tear in the tissue lining the anus or lower rectum. This causes pain and bleeding.")
	condition_add(anal_fissure)
	
	question1_anal_fissure = add_question(anal_fissure,"What sort of problem is an anal fissure?")
	answer1_question1 = add_answer(question1_anal_fissure,doctor5,"An anal fissure is a tear in the lining of the intestine in the area of your anal opening.This can result in pain while having a bowel movement and some bleeding too.")
	answer2_question1 = add_answer(question1_anal_fissure,doctor2,"Tear of lining in the anus; tearing type pain during defecation, sometimes bleeding, or infection.Can be treated like hemorrhoids initially, e.g. Soaks, soothing suppositories. Can recur;sometimes sphincter can be too tight; rx'd with meds, injections, or surgery. To decrease the spasm.")
	
	question2_anal_fissure = add_question(anal_fissure,"How does an anal fissure cause constipation?")
	answer1_question1 = add_answer(question2_anal_fissure,doctor1,"In general, anal fissures do not cause constipation, unless you are intentionally stopping yourself from having a bowel movement because you're aware of the fissure.On the other hand, hard stools that happen when you are constipated can cause a fissure.")
	
	# add medication 
	botulinum_toxin = topic_add_sub(anal_fissure,"Botulinum toxin","Botulism is a rare but serious illness caused by Clostridium botulinum bacteria. The bacteria may enter the body through wounds, or they may live in improperly canned or preserved food.")
	medication_add(botulinum_toxin)
	
	Nitroglycerin = topic_add_sub(anal_fissure,"Nitroglycerin","Nitroglycerin dilates the blood vessels around the heart to relieve heart pain or 'angina'. It comes in both a pump spray and tablet form. There are several cautions when using this medication so always discuss with your doctor and pharmacist.")
	medication_add(Nitroglycerin)
	
	Hydrocortisone = topic_add_sub(anal_fissure,"Hydrocortisone","Cortisone is a naturally produced hormone in the body, produced by the adrenal glands. It is often used as a potent medication for inflammatory disease. In serious cases, it is a 'wonder' drug, and can be life saving. However, long and continuous use can cause many serious and uncomfortable side effects. Hydrocortisone is a topical skin variety and much less potent than cortisone.")
	medication_add(Hydrocortisone)
	
	Petroleum_jelly = topic_add_sub(anal_fissure,"Petroleum jelly","Petroleum jelly or vasoline can be used as a barrier ointment for like diaper rash, eczema and other skin conditions.")
	medication_add(Petroleum_jelly)
	
	#add condition 
	Anal_and_rectal_diseases = topic_add_sub(anal_fissure,"Anal and rectal diseases","Anal and rectal diseases are conditions that effect the bottom end of the digest tract, including the anus. These conditions may include hemorrhoids, cancer, warts, and many other problems.")
	condition_add(Anal_and_rectal_diseases)
	
	#add symptom 
	Painful_bowel_movements = topic_add_sub(anal_fissure,"Painful bowel movements","Having pain while engaged in normal bodily funstions is not normal. Pain may be due to hemeriod that are inflamed , fistulas , fissures, tumors, or trauma of perverted behaviors.")
	symptom_add(Painful_bowel_movements)
	
	Anal_pain = topic_add_sub(anal_fissure,"Anal pain","Anal pain can be caused by many different conditions - hemorrhoids, constipation, fissures, absecss, fungal infection. More concerning causes of anal pain include cancer. It's important not to discount any anal pain or bleeding - it's always good to have it evaluated by your physician.")
	symptom_add(Anal_pain)
	
	Blood_in_stool = topic_add_sub(anal_fissure,"Blood in stool","Blood in the stool of babies is always a concern and should be investigated. Some of the causes include food allergies, infection of the bowels (bacterial gastroenteritis), anal fissure, and rarely, intussusception.")
	symptom_add(Blood_in_stool)
	
	#add procedure 
	anorectal_manometry = topic_add_sub(anal_fissure,"Anorectal manometry","Anorectal manometry is a test performed to evaluate patients with constipation or fecal incontinence. This test measures the pressures of the anal sphincter muscles, the sensation in the rectum, and the neural reflexes that are needed for normal bowel movements.")
	procedure_add(anorectal_manometry)
	
	#add topic COPD
	copd = topic_add("COPD","COPD may include chronic bronchitis, emphysema, or both. Chronic bronchitis is the production of increased mucus caused by inflammation. Bronchitis is considered chronic if you cough and produce excess mucus most days for three months in a year, two years in a row. Emphysema is a disease that damages the air sacs and/or the smallest breathing tubes in the lungs. Common day-to-day COPD symptoms.")
	condition_add(copd)
	
	question1_copd = add_question(copd,"What is the simplest definition of chronic obstructive pulmonary disease (copd)?")
	answer1_question1 = add_answer(question1_copd,doctor3,"COPD is a disease characterized by the presence of chronic, irreversible airway obstruction as measured by pulmonary function testing.The disease is incurable but there are treatments available so see your doctor for diagnosis and treatment. The most important treatment is smoking cessation since smoking is the main etiology of this disease.")
	answer2_question1 = add_answer(question1_copd,doctor2,"A disease characterized by airflow obstruction that is not completely reversible as a consequence of tobacco use or exposure to particulate airborne matter.")
	
	question2_copd = add_question(copd,"How does COPD affect your overall lifestyle?")
	answer1_question1 = add_answer(question2_copd,doctor4,"COPD usually causes shortness of breath, especially with exertion, and decreased exercise capacity, causing fatigue with minimal exercise.")
	answer2_question1 = add_answer(question2_copd,doctor2,"COPD may decrease your exercise potential and case breathlessness with activities such as running, climbing stairs, lifting and having sex.As the disease progresses shortness of breath cab occur with more mudane activity such as walking, fixing meals, bathing and dressing.")
	
	#add medication 
	Albuterol_and_ipratropium = topic_add_sub(copd,"Albuterol and ipratropium","Albuterol|ipratropium is an asthma beta receptor stimulator which is a kind of asthma drug (lung drug).")
	medication_add(Albuterol_and_ipratropium)
	
	Salmeterol_and_fluticasone = topic_add_sub(copd,"Salmeterol and fluticasone","Prevents symptoms of asthma or COPD (chronic obstructive pulmonary disease). This medicine contains a steroid and a long-acting beta-agonist (LABA).")
	medication_add(Salmeterol_and_fluticasone)
	
	Pneumococcal_vaccine = topic_add_sub(copd,"Pneumococcal vaccine","Pneumococcal vaccine is an immunization which is a kind of immune system affecting drug.")
	medication_add(Pneumococcal_vaccine)
	
	Budesonide_and_formoterol = topic_add_sub(copd,"Budesonide and formoterol","Prevents asthma attacks. This medicine may be used with other asthma medicines. It is also used to treat chronic obstructive pulmonary disease (COPD), including chronic bronchitis and emphysema. This medicine is a combination of a steroid medicine and a bronchodilator.")
	medication_add(Budesonide_and_formoterol)
	
	#add condtion 
	Lung_diseases = topic_add_sub(copd,"Lung diseases","Lung diseases are diseases that interfere with the lung's ability to exchange oxygen. They includes genetic diseases, infections, asthma, trauma, and cancer.")
	condition_add(Lung_diseases)
	
	#add symptom 
	fatigue = topic_add_sub(copd,"Fatigue","Fatigue (also called exhaustion, tiredness, languidness, languor, lassitude, and listlessness) is a subjective feeling of tiredness which is distinct from weakness, and has a gradual onset. Unlike weakness, fatigue can be alleviated by periods of rest. Fatigue can have physical or mental causes.")
	
	headache = topic_add_sub(copd,"Headache","Also called cephalalgia, is pain anywhere in the region of the head or neck, & can be a symptom of a number of conditions affecting those areas. It originates from pain-sensitive structures such as cranium, muscles, nerves, vessels, subcutaneous tissues, eyes, ears, sinuses & mucous membranes. It is non-specific symptom & can be primary such as tension ha, or secondary such as organic causes.")
	
	fever = topic_add_sub(copd,"fever","Fever is the temporary increase in the body's temperature in response to some disease or illness. A child has a fever when the temperature is at or above one of these levels: * 100.4")
	
	cough = topic_add_sub(copd,"Cough","Coughing is an important way to keep your throat and airways clear. However, excessive coughing may mean you have an underlying disease or disorder. Some coughs are dry, while others are considered productive. A productive cough is one that brings up mucus.")
	
	Difficulty_breathing_when_lying_down = topic_add_sub(copd,"Difficulty_breathing_when_lying_down","Difficulty breathing when lying is a clinical finding in which lying down leads to increased effort with breath such that there is discomfort. This can occur with heart failure, due to some fluid getting into the lungs")
	symptom_add(Difficulty_breathing_when_lying_down)
	
	Decreased_mental_status = topic_add_sub(copd,"Decreased mental status","Decreased or altered mental status is a clinical description of an individual who is not oriented to person, place or time. It can be a symptom of infection, stroke, seizures, or any thing that messes with the brain.")
	symptom_add(Decreased_mental_status)
	
	Leg_swelling = topic_add_sub(copd,"Leg swelling","Leg swelling could be due to infection, allergy, poor circulation/congestive heart failure or lymphadema. If you have leg swelling you should see your doctor.")
	symptom_add(Leg_swelling)
	
	Clubbing = topic_add_sub(copd,"Clubbing","Clubbing is a condition where the nails and tips of the fingers become rounded and somewhat enlarged (so that they look like clubs). The reason this occurs is unknown, but it is associated with breathing problems or lung diseases.")
	symptom_add(Clubbing)
	
	Chest_tightness = topic_add_sub(copd,"Chest tightness","Chest tightness is a squeezing sensation or sense of heaviness within the chest. If this sensation occurs in response to the heart not receiving enough blood, it is called angina pain.")
	symptom_add(Chest_tightness)
	
	Wheezing = topic_add_sub(copd,"Wheezing","Wheezing is a high-pitched whistling sound during breathing. It occurs when air flows through narrowed breathing tubes (bronchi).")
	symptom_add(Wheezing)
	
	#add porcedure
	Basic_metabolic_panel = topic_add_sub(copd,"Basic metabolic panel","The basic metabolic panel (bmp) is a panel of blood tests that serves as an initial broad medical screening tool. The bmp provides a rough check of kidney function and electrolyte and fluid balance. The bmp is an smaller version of the comprehensive metabolic panel (cmp), which also includes liver tests. A bmp (or cmp) is usually ordered as part of a routine physical exam.")
	procedure_add(Basic_metabolic_panel)
	
	Complete_blood_count = topic_add_sub(copd,"Complete blood count","Share on twitter bookmark & share printer-friendly version a complete blood count (CBC) test measures the following: •the number of red blood cells (rbc count) •the number of white blood cells (wbc count) •the total amount of hemoglobin in the blood •the fraction of the blood composed of red blood cells (hematocrit).")
	procedure_add(Complete_blood_count)
	
	CT_of_chest = topic_add_sub(copd,"CT of chest","A chest computed tomography (to-MOG-ra-fee) scan, or chest CT scan, is a painless, noninvasive test. It creates precise pictures of the structures in your chest, such as your lungs.")
	procedure_add(CT_of_chest)
	
	Xray_of_chest = topic_add_sub(copd,"Xray of chest","A chest x-ray is the basic radiographic study for evaluation of the heart and lungs. It usually consists of 2 views: postero-anterior and lateral. The image is now usually acquired digitally with the sensor placed against the front of the chest for the pa view and on the left side of the chest for the lateral view. Pneumonia, heart enlargement, CHF and many other conditions may be assessed.")
	procedure_add(Xray_of_chest)
	
	Electrocardiogram = topic_add_sub(copd,"Electrocardiogram","Electrocardiogram (ecg, ekg) is a print-out of the electrical forces detected by electrodes on the chest wall, as electricity travels through the heart with each heart beat. The electrodes are placed in different positions, and each position 'sees' the electrical activity of the heart from its own vantage point. Abnormalities in signal detected at chest surface can indicate underlying disease.")
	procedure_add(Electrocardiogram)
	
	Oxygen_saturation = topic_add_sub(copd,"Oxygen saturation","Oxygen saturation is a measure of how much oxygen the blood is carrying as a percentage of the maximum it could carry.")
	procedure_add(Oxygen_saturation)
	
	Pulmonary_function_test = topic_add_sub(copd,"Pulmonary function test","Pulmonary function tests is a term used to describe a group of tests done to determine lung function. Spirometry measures the amount of air that can be taken in as well as the flow rate of forcefully exhaled air . A graph is generated and can be used to determine lung function. Likewise lung volumes and diffusing capacity determine the capacity as well as the oxygen exchange function.")
	procedure_add(Pulmonary_function_test)
	
	Spirometry = topic_add_sub(copd,"Spirometry","A spirometry is a measurement of velocity (speed) of air coming in & out of the lungs which equals the diameter of the airways. This an indirect measument of the lung function diffeent patterns are posible & direct us as specialist to diagnosed or suggest certain conditions.")
	procedure_add(Spirometry)
	
	Sputum_gram_stain_and_culture = topic_add_sub(copd,"Sputum gram stain and culture","The sputum Gram stain is a laboratory test ordered when a doctor suspects that a patient’s respiratory symptoms may be caused by a bacterial infection.")
	procedure_add(Sputum_gram_stain_and_culture)
	
	#add vaccination:
	Diphtheria = topic_add("Diphtheria vaccine","Diphtheria vaccine is a vaccine used against Corynebacterium diphtheriae, the agent that causes diphtheria. It use has resulted in a more than 90% decrease in number of cases globally between 1980 and 2000.")
	Di_va=medication_add(Diphtheria)
	vaccination_add(Di_va)
	
	Hepatitis_A = topic_add("Hepatitis A vaccine","Hepatitis A vaccine is a vaccine against the hepatitis A virus. There are two types of vaccines: one type contains inactivated hepatitis A virus, the other contains a live but attenuated virus. Both types stimulate active immunity against a future infection.")
	He_va = medication_add(Hepatitis_A)
	vaccination_add(He_va)
	
	Hepatitis_B = topic_add("Hepatitis B vaccine","Hepatitis B vaccine is a vaccine for the prevention of hepatitis B, an infection caused by the hepatitis B virus (HBV).")
	Heb_va = medication_add(Hepatitis_B)
	vaccination_add(Heb_va)
	
	Hib = topic_add("Hib vaccine","Haemophilus influenzae type B vaccine (Hib janan or PRP vaccine[1]) is a conjugate vaccine developed for the prevention of invasive disease caused by Haemophilus influenzae type b bacteria.")
	Hib_va = medication_add(Hib)
	vaccination_add(Hib_va)
	
	Hpv = topic_add("HPV vaccine","Human papilloma virus (HPV) vaccines may prevent infections by certain types of human papillomavirus associated with the development of cervical cancer, genital warts, and other cancers.")
	Hpv_va = medication_add(Hpv)
	vaccination_add(Hpv_va)
	
	Influenza = topic_add("Influenza vaccine","The influenza vaccine, also known as flu shot, is an annual vaccination using a vaccine that is specific for a given year to protect against the highly variable influenza virus.")
	In_va = medication_add(Influenza)
	vaccination_add(In_va)
	
	Measles = topic_add("Measles vaccine","The measles, mumps, and rubella (MMR) vaccine is recommended for all children. It protects against three potentially serious illnesses. It is a two-part vaccination, and in most states, you must prove your children have gotten it before they can enter school.")
	Me_va = medication_add(Measles)
	vaccination_add(Me_va)
	
	Meningococcal = topic_add("Meningococcal vaccine","Meningococcal vaccine refers to any one of a number of vaccines used against Neisseria meningitidis, a bacterium that causes meningitis, meningococcemia, septicemia, and rarely carditis, septic arthritis, or pneumonia.")
	Mening_va = medication_add(Meningococcal)
	vaccination_add(Mening_va)
	
	mumps = topic_add("Mumps vaccine","RIT 4385 is a newer strain derived from the Jeryl Lynn strain. It was invented by Maurice Hilleman. MMR Vaccine (Measles, Mumps, Rubella Vaccine) is the most commonly used form of the vaccine, formulated in combination with vaccines for measles and rubella.")
	mumps_va = medication_add(mumps)
	vaccination_add(mumps_va)
	
	pertussis_vaccine = topic_add("Pertussis vaccine","Pertussis vaccine is a vaccine used against Bordetella pertussis.They are effective and are recommended for routine use by the World Health Organization and the Center for Disease Control and Prevention.The vaccine saved over an estimated half a million lives in 2002.")
	pertu_va = medication_add(pertussis_vaccine)
	vaccination_add(pertu_va)
	
	pneumococcal = topic_add("Pneumococcal vaccine","A pneumococcal vaccine is a vaccine against Streptococcus pneumoniae.")
	pneumococcal_va = medication_add(pneumococcal)
	vaccination_add(pneumococcal_va)
	
	polio = topic_add("Polio vaccine","Two polio vaccines are used throughout the world to combat poliomyelitis (or polio). The first was developed by Jonas Salk through the use of HeLa cells and first tested in 1952. Announced to the world by Dr Thomas Francis Jr. on 12 April 1955")
	polio_va = medication_add(polio)
	vaccination_add(polio_va)
	
	rotavirus = topic_add("Rotavirus vaccine","A rotavirus vaccine protects children from rotaviruses, which are the leading cause of severe diarrhea among infants and young children.")
	rotavirus_va = medication_add(rotavirus)
	vaccination_add(rotavirus_va)
	
	Rubella = topic_add("Rubella vaccine","Rubella vaccine is a vaccine used against rubella.")
	rubella_va = medication_add(Rubella)
	vaccination_add(rubella_va)
	
	zoster = topic_add("Zoster vaccine","The zoster vaccine (trade name Zostavax) is a live vaccine developed by Merck & Co. that has been shown to reduce the incidence of herpes zoster (known as shingles) by 51.3% in a study of 38,000 adults aged 60 and older who received the vaccine. The vaccine also reduced by 66.5% the number of cases of postherpetic neuralgia and reduced the severity and duration of pain and discomfort associated with shingles, by 61.1%.")
	zoster_va = medication_add(zoster)
	vaccination_add(zoster_va)
	
	tetanus = topic_add("Tetanus vaccine","Tetanus vaccine is a vaccine composed of deactivated tetanus toxins. This vaccine is immunogenic but not pathogenic and is used to prevent an individual from contracting tetanus.")
	tetanus_va = medication_add(tetanus)
	vaccination_add(tetanus_va)
	
	varicella = topic_add("Varicella vaccine","The varicella vaccine is a live (attenuated) virus administered to protect against the viral disease commonly known as chickenpox caused by the varicella zoster virus (VZV).")
	varicella_va = medication_add(varicella)
	vaccination_add(varicella_va)
	
	cholera = topic_add("Cholera vaccine","Cholera vaccines are vaccines that are effective in preventing cholera.")
	cholera_va = medication_add(cholera)
	vaccination_add(cholera_va)
	
	japanese_encephalitis = topic_add("Japanese encephalitis vaccine","Japanese encephalitis vaccine is a vaccine used against Japanese encephalitis.")
	japanese_va = medication_add(japanese_encephalitis)
	vaccination_add(japanese_va)
	
	rabies = topic_add("Rabies vaccine","A rabies vaccine is a vaccine used to prevent rabies.There are a number of available vaccines that are both safe and effective.")
	rabies_va = medication_add(rabies)
	vaccination_add(rabies_va)
	
	tuberculosis = topic_add("Tuberculosis vaccine","Tuberculosis vaccines are vaccinations intended for the prevention of tuberculosis.")
	tuberculosis_va = medication_add(tuberculosis)
	vaccination_add(tuberculosis_va)
	
	typhiod = topic_add("Typhoid vaccine","Typhoid vaccines are vaccines developed to prevent typhoid fever.")
	typhiod_va = medication_add(typhiod)
	vaccination_add(typhiod_va)
	
	yellow_fever = topic_add("Yellow fever vaccine","Yellow fever vaccine is a vaccine used against yellow fever.")
	yellow_fever_va =medication_add(yellow_fever)
	vaccination_add(yellow_fever_va)
	
def category_add(title):
	cat = Category.objects.get_or_create(title=title)[0]
	
	return cat 

def goal_add(title,related_cat):
	goal = Goal.objects.get_or_create(title=title,related_category=related_cat)[0]
	
	return goal 

def topic_add(title,definition):
	try:
		topic  = Topic.objects.get(title=title)
	except Topic.DoesNotExist:
		topic = Topic(title=title,definition=definition)
		topic.save()

	notification = Notification.objects.get_or_create(topic=topic)
	return topic 

def medication_add(topic):
	me = Medication.objects.get_or_create(topic=topic)[0]
	
	return me
	
def vaccination_add(medication):
	
	va = Vaccination.objects.get_or_create(medication=medication)[0]
	
	return va 

def condition_add(topic):
	con = Condition.objects.get_or_create(topic=topic)[0]
	
	return con

def symptom_add(topic):
	sym = Symptom.objects.get_or_create(topic=topic)[0]
	
	return sym 
	
def procedure_add(topic):
	pro = Procedure.objects.get_or_create(topic=topic)[0]
	
	return pro 
	
def risk_factor_add(topic):
	risk = Riskfactor.objects.get_or_create(topic=topic)[0]
	
	return risk 
	
def topic_add_sub(topic_related,title,definition):
	try:
		topic  = Topic.objects.get(title=title)
	except Topic.DoesNotExist:
		topic = Topic(title=title,definition=definition)
		topic.save()
	topic.related_topic.add(topic_related)
	topic.save()
	notification = Notification.objects.get_or_create(topic=topic)
	return topic

def goal_add_sub(goal_related,title,definition):
	try:
		topic = Topic.objects.get(title=title)
	except:
		topic = Topic(title=title, definition=definition)
		topic.save() 
	topic_goal = TopicAndGoal.objects.get_or_create(topic=topic, goal=goal_related)
	
	notification = Notification.objects.get_or_create(topic=topic)
	
	return topic 
	
def add_user(username, email,password):
	u = User.objects.get_or_create(username=username, email=email)[0]
	u.set_password(password)
	u.save()
	return u 
	
def add_doctor(username,email,password,name,specialty,gender,school,license,degree,year,address):
	user = add_user(username,email,password)
	
	doctor = Doctor.objects.get_or_create(user=user,name=name,specialty=specialty,gender=gender,school=school,license=license,degree=degree,year=year,address=address)[0]
	doctor_record = DoctorRecord.objects.get_or_create(doctor=doctor)
	return doctor
	
def add_listitem(related_checklist,title,priority,frequency):
	item = ListItem.objects.get_or_create(title=title, priority=priority, frequency = frequency, related_checklist = related_checklist)[0]
	
	return item 
	
def add_checklist(related_goal,related_doctor):
	checklist = CheckList.objects.get_or_create(related_goal = related_goal,related_doctor=related_doctor)[0]
	notification = Notification.objects.get_or_create(checklist=checklist)
	return checklist 
	
def add_question(related_topic,title):
	question = Question.objects.get_or_create(title=title)[0]
	question.related_topic=related_topic
	question.save()
	notification = Notification.objects.get_or_create(question=question)
	return question 

def add_answer(related_question,from_doctor,detail):
	answer = Answer.objects.get_or_create(detail=detail,related_question=related_question,from_doctor=from_doctor)[0]
	
	return answer 

def add_question_goal(goal,title):
	question = Question.objects.get_or_create(title=title)[0]
	question.related_goal = goal 
	question.save() 
	
	notification = Notification.objects.get_or_create(question=question)
	return question
	
def add_question_sub(question_related,title):
	question = Question.objects.get_or_create(title=title)[0]
	relation1 = QuestionRelate.objects.get_or_create(question=question,question_related=question_related)
	relation2 = QuestionRelate.objects.get_or_create(question=question_related,question_related=question)
	
	notification = Notification.objects.get_or_create(question=question)
	return question 
	
if __name__ == '__main__':
	print "starting population script...."
	populate() 