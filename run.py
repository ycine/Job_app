from main_page import JobGetter

pracuj = JobGetter()
connect = pracuj.connect_to_webpage()
print('JobGetter - connect_to_webpage - succes')

define = pracuj.define_jobs(JobGetter.url_job, JobGetter.job_date_added)
print('JobGetter - define_jobs - succes')

number_of_offers = pracuj.get_number_of_offers(define)
print('JobGetter -  get_number_of_offers - succes')


# get_offers = pracuj.get_offers_from_page(define)
# print('JobGetter - get_offers_from_page - succes')


pracuj.loop_over_the_pages(number_of_offers, define)
print('JobGetter - loop_over_the_pages - succes')