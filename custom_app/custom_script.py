import frappe



import frappe
import requests
from frappe import _
from frappe.utils import today
import random

@frappe.whitelist()
def fetch_sales_orders(cid=None):
    # Fetch sales orders based on the customer ID and docstatus
    sales_orders = frappe.get_list(
        'Sales Order',
        filters={'customer': cid, 'status': ('in', ["Draft", "On Hold", "To Deliver and Bill", "To Bill", "To Deliver"])},
        fields=['name', 'transaction_date', 'advance_paid', 'grand_total', 'customer', 'customer_name', 'status']
    )

    # Return a list of dictionaries with sales order details
    return [
        {
            'sales_order': so.name,
            'transaction_date': so.transaction_date,
            'advance_paid': so.advance_paid,
            'total': so.grand_total,
            'cid': so.customer,
            'customer_name': so.customer_name,
            'sales_status': so.status
        }
        for so in sales_orders
        if so.grand_total != so.advance_paid
    ]

#############################################################################################################################


# # Aisensy integration for Sales Invoice

# @frappe.whitelist(allow_guest=True)
# def aisensy(docname, customer,from_date,to_date,total,new_mobile,razorpay_payment_link):
#     try:
#         ai_sensy_api = frappe.get_doc('Ai Sensy Api')

#         application_url = ai_sensy_api.application_url
#         ai_sensy_url = ai_sensy_api.ai_sensy_url
#         ai_sensy_api1 = ai_sensy_api.ai_sensy_api
#         # Check if Sales Invoice exists
#         if not frappe.get_value('Sales Invoice', docname):
#             frappe.msgprint(_("Sales Invoice {0} not found.").format(docname))
#             return

#         # Fetch the Sales Invoice document
#         sales_invoice = frappe.get_doc('Sales Invoice', docname)
#         erpnext_url = application_url
#         # Replace the following URL with the actual AI Sensy API endpoint
#         sensy_api_url = ai_sensy_url

#         sales_invoice_url = frappe.utils.get_url(
#             f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name={docname}&format=Sales%20Invoice%20Format&no_letterhead=0&letterhead=LSA&settings=%7B%7D&_lang=en"
#         )
#         pdf_url = f"{erpnext_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name={docname}&format=Standard"

#         # pdf_url1 = frappe.utils.get_url(
#         #     f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name={docname}&format=Standard"
#         # )

#         # Example payload to send to the AI Sensy API
#         payload = {
#             "apiKey": ai_sensy_api1,  # Replace with your actual API key
#             "campaignName": "lsa_saleorder_invoice_with_payment_link",
#             "destination": new_mobile,
#             "userName": customer,
#             "templateParams": [
#                 customer,
#                 from_date,
#                 to_date,
#                 total,
#                 razorpay_payment_link
#             ],
#             "media": {
#                 "url": sales_invoice_url,
#                 "filename": docname
#             }
#         }

#         # Make a POST request to the AI Sensy API
#         response = requests.post(sensy_api_url, json=payload)

#         # Check if the request was successful (status code 200)
#         if response.status_code == 200:
#             # Log the API response for reference
#             frappe.logger().info(f"AI Sensy response: {response.text}")

#             # You can update the Sales Invoice or perform other actions based on the API response
#             # sales_invoice.custom_field = response.json().get('result')
#             # sales_invoice.save()

#             frappe.msgprint(_("WhatsApp Message Sent successfully : {0}").format(response.text))
#         else:
#             # Log the error and provide feedback to the user
#             frappe.logger().error(f"Sensy API Error: {response.text}")
#             frappe.msgprint(_("WhatsApp message failed to send!. Please try again Later."))

#     except requests.exceptions.RequestException as e:
#         # Log the exception and provide feedback to the user
#         frappe.logger().error(f"Network error: {e}")
#         frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later."))

#     except Exception as e:
#         # Log the exception and provide feedback to the user
#         frappe.logger().error(f"Custom Button Script Error: {e}")
#         frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later."))



# ##########################################################################################
# #Razorpay Payment Link For Sales Invoice
# import razorpay


# @frappe.whitelist()
# def create_razorpay_order(amount, invoice_name,customer,customer_name):
#     # Your Razorpay API key and secret
#     razorpay_api = frappe.get_doc('Razorpay Api')

#     razorpay_api_url = razorpay_api.razorpay_api_url
#     razorpay_api_key = razorpay_api.razorpay_api_key
#     razorpay_api_secret = razorpay_api.razorpay_secret
    
    
#     razorpay_key_id = razorpay_api_key
#     razorpay_key_secret = razorpay_api_secret

#     # Specify the custom Razorpay API URL
#     custom_razorpay_api_url = razorpay_api_url

#     # Convert the amount to an integer (representing paise)
#     amount_in_paise = int(float(amount) * 100)

#     # Create a Razorpay order
#     order_params = {
#         "amount": amount_in_paise,
#         "currency": "INR",
#         "accept_partial": True,
#         "first_min_partial_amount": 100,
#         "description": invoice_name,
#         "notes": {
#             "invoice_name": invoice_name
#         },
#         # "accept_partial": True,
#         # "expire_by": 1691097057,
#         "reference_id": invoice_name
#     }
 
#     try:
#         # Use the requests library to send a POST request
#         order = requests.post(
#             custom_razorpay_api_url,
#             json=order_params,
#             auth=(razorpay_key_id, razorpay_key_secret)  # Add authentication here
#         )

#         # Check if the request was successful (status code 2xx)
#         order.raise_for_status()

#         # Get the JSON response
#         response_json = order.json()

#         # Extract short_url from the response
#         short_url = response_json.get('short_url')

#         # Optionally, you can store custom_payment_link in a database or use it as needed

#         # Update the Sales Invoice document with the short_url
#         doc = frappe.get_doc('Sales Invoice', invoice_name)
#         doc.razorpay_payment_url = short_url
#         doc.save()

#         frappe.msgprint(f'Successfully created Razorpay order. Short URL: {short_url}')

#     except requests.exceptions.HTTPError as errh:
#         frappe.msgprint(f'HTTP Error: {errh}')
#     except requests.exceptions.ConnectionError as errc:
#         frappe.msgprint(f'Error Connecting: {errc}')
#     except requests.exceptions.Timeout as errt:
#         frappe.msgprint(f'Timeout Error: {errt}')
#     except requests.exceptions.RequestException as err:
#         frappe.msgprint(f'Request Exception: {err}')



####################################################################################################################

# Aisensy integration for Sales Order


@frappe.whitelist(allow_guest=True)
def aisensy_sales_order(docname,customer_id, customer,from_date,to_date,total,new_mobile,razorpay_payment_link):
    try:
        # frappe.msgprint(from_date)
        # pass
        ai_sensy_api = frappe.get_doc('Ai Sensy Api')

        application_url = ai_sensy_api.application_url
        ai_sensy_url = ai_sensy_api.ai_sensy_url
        ai_sensy_api1 = ai_sensy_api.ai_sensy_api
        # Check if Sales Order exists
        if not frappe.get_value('Sales Order', docname):
            frappe.msgprint(_("Sales Order {0} not found.").format(docname))
            return

        # Fetch the Sales Order document
        sales_invoice = frappe.get_doc('Sales Order', docname)
        erpnext_url = application_url
        # Replace the following URL with the actual AI Sensy API endpoint
        sensy_api_url = ai_sensy_url

        sales_order_url = frappe.utils.get_url(
            f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Order&name={docname}&format=Sales%20Order%20Format&no_letterhead=0&letterhead=LSA&settings=%7B%7D&_lang=en"
        )
        
        # pdf_url = f"{erpnext_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name={docname}&format=Standard"

        # pdf_url1 = frappe.utils.get_url(
        #     f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Invoice&name={docname}&format=Standard"
        # )
        # Example payload to send to the AI Sensy API
        payload = {
            "apiKey": ai_sensy_api1,  # Replace with your actual API key
            "campaignName": "lsa_saleorder_invoice_with_payment_link",
            "destination": new_mobile,
            "userName": customer,
            "templateParams": [
                customer,
                from_date,
                to_date,
                # format_date(from_date, "dd-mmm-yyyy"),  # Format from_date
                # format_date(to_date, "dd-mmm-yyyy"),
                total,
                razorpay_payment_link
            ],
            "media": {
                "url": sales_order_url,
                # "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "filename": docname
            }
        }

        # Make a POST request to the AI Sensy API
        response = requests.post(sensy_api_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Log the API response for reference
            frappe.logger().info(f"AI Sensy response: {response.text}")

            # You can update the Sales Invoice or perform other actions based on the API response
            # sales_invoice.custom_field = response.json().get('result')
            # sales_invoice.save()

            frappe.msgprint(_("WhatsApp Message Sent successfully : {0}").format(response.text))
            whatsapp_message_log = frappe.new_doc('WhatsApp Message Log')
            whatsapp_message_log.sales_order = docname
            whatsapp_message_log.customer = customer_id
            whatsapp_message_log.sender = frappe.session.user  # Add the sender information
            whatsapp_message_log.send_date = frappe.utils.now_datetime()
            # whatsapp_message_log.from_date = from_date
            # whatsapp_message_log.to_date = to_date
            whatsapp_message_log.total_amount = total
            whatsapp_message_log.mobile_no = new_mobile
            whatsapp_message_log.razorpay_payment_link = razorpay_payment_link
            whatsapp_message_log.insert(ignore_permissions=True)
        else:
            # Log the error and provide feedback to the user
            frappe.logger().error(f"Sensy API Error: {response.text}")
            frappe.msgprint(_("WhatsApp message failed to send!. Please try again Later."))

    except requests.exceptions.RequestException as e:
        # Log the exception and provide feedback to the user
        frappe.logger().error(f"Network error: {e}")
        frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later."))

    except Exception as e:
        # Log the exception and provide feedback to the user
        frappe.logger().error(f"Custom Button Script Error: {e}")
        frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later."))


###########################################################################################################################


    #Razorpay Payment Link For Sales Order
import razorpay


@frappe.whitelist()
def create_razorpay_payment_link_sales_order(amount, invoice_name,customer,customer_name,from_date,to_date,actual_amount):
    payment_links = frappe.get_all("Payment Link Log",
                                   filters={"sales_order":invoice_name,"enabled":1})
    if payment_links:
        return
    
    # Your Razorpay API key and secret
    razorpay_api = frappe.get_doc('Razorpay Api')

    razorpay_api_url = razorpay_api.razorpay_api_url
    razorpay_api_key = razorpay_api.razorpay_api_key
    razorpay_api_secret = razorpay_api.razorpay_secret
    
    
    razorpay_key_id = razorpay_api_key
    razorpay_key_secret = razorpay_api_secret

    # Specify the custom Razorpay API URL
    custom_razorpay_api_url = razorpay_api_url

    # Convert the amount to an integer (representing paise)
    amount_in_paise = int(float(amount) * 100)
    # print("Testing==============")
    # Create a Razorpay order
    order_params = {
        "amount": amount_in_paise,
        "currency": "INR",
        # "accept_partial": "0",
        # "first_min_partial_amount": 100,
        "description": f"Sales order for the period from {from_date} to {to_date}",
        "notes": {
            "invoice_name": invoice_name
        },
        # "accept_partial": False,
        # "expire_by": 1691097057,
        "reference_id": invoice_name,
        "callback_url": f"https://online.lsaoffice.com/api/method/lsa.pankaj1.get_razorpay_payment_details?customer={customer}&actual_amount={actual_amount}",
        "callback_method": "get"
    }
 
    try:
        # Use the requests library to send a POST request
        # order = requests.post(
        #     custom_razorpay_api_url,
        #     json=order_params,
        #     auth=(razorpay_key_id, razorpay_key_secret)  # Add authentication here
        # )

        # # Check if the request was successful (status code 2xx)
        # order.raise_for_status()

        def generate_pl(custom_razorpay_api_url,order_params,auth,reference_id,link_js=None,status=400):
            if status!=200:

                random_number = random.randint(100, 999)

                reference_id_with_rn=reference_id+'-'+str(random_number)

                order_params["reference_id"]=reference_id_with_rn

                link_json = requests.post(
                    custom_razorpay_api_url,
                    json=order_params,
                    auth=(razorpay_key_id, razorpay_key_secret)  # Add authentication here
                )
                status=link_json.status_code

                return generate_pl(custom_razorpay_api_url,order_params,auth,reference_id,link_json,status)
            else:
                return link_js
            
        auth=(razorpay_key_id, razorpay_key_secret)
        order=generate_pl(custom_razorpay_api_url,order_params,auth,invoice_name)

        # Get the JSON response
        response_json = order.json()
        link_id=response_json.get('id')

        # Extract short_url from the response
        short_url = response_json.get('short_url')

        # Optionally, you can store custom_payment_link in a database or use it as needed

        # Update the Sales Invoice document with the short_url
        doc = frappe.get_doc('Sales Order', invoice_name)
        doc.custom_razorpay_payment_url = short_url
        doc.save()

        new_payment_link = frappe.get_doc({
            "doctype": "Payment Link Log",
            "customer_id": customer,
            "sales_order":invoice_name,
            "total_amount":amount,
            "link_short_url":short_url,
            "link_id":link_id,

        })
        new_payment_link.insert()

        frappe.msgprint(f'Successfully created Razorpay order. Short URL: {short_url}')
       

    except requests.exceptions.HTTPError as errh:
        #frappe.msgprint(f'HTTP Error: {errh}')
        frappe.msgprint(f'Failed to generate the Razorpay payment link:{errh}')
    except requests.exceptions.ConnectionError as errc:
        #frappe.msgprint(f'Error Connecting: {errc}')
        frappe.msgprint(f'Failed to generate the Razorpay payment link:{errc}')
    except requests.exceptions.Timeout as errt:
        #frappe.msgprint(f'Timeout Error: {errt}')
        frappe.msgprint(f'Failed to generate the Razorpay payment link:{errt}')
    except requests.exceptions.RequestException as err:
        #frappe.msgprint(f'Request Exception: {err}')
        frappe.msgprint(f'Failed to generate the Razorpay payment link:{err}')




@frappe.whitelist(allow_guest=True)
def get_razorpay_payment_details(razorpay_payment_link_id,razorpay_payment_link_reference_id,customer,actual_amount):
    try:
        razorpay_api = frappe.get_doc('Razorpay Api')

        # razorpay_api_url = razorpay_api.razorpay_api_url
        razorpay_api_key = razorpay_api.razorpay_api_key
        razorpay_api_secret = razorpay_api.razorpay_secret
        
        
        razorpay_key_id = razorpay_api_key
        razorpay_key_secret = razorpay_api_secret

        # Specify the custom Razorpay API URL
        custom_razorpay_api_url = f'https://api.razorpay.com/v1/payment_links/{razorpay_payment_link_id}'

        # Make a request to the custom Razorpay API URL
        response = requests.get(
            custom_razorpay_api_url,
            auth=(razorpay_key_id, razorpay_key_secret)  # Add authentication here
        )

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            razorpay_response = response.json()
            # Navigate through the JSON structure to extract amount_paid
            # amount_paid = razorpay_response.get('amount_paid')
            # final_amount = int(float(amount_paid) / 100)
            payments = razorpay_response.get('payments')
            if payments:
                most_recent_payment = max(payments, key=lambda x: x['created_at'])
                # payment_id = most_recent_payment.get('payment_id')
                payment_amount = most_recent_payment.get('amount')
                # payment_status = most_recent_payment.get('status')
                final_amount = int(float(payment_amount) / 100)
                # print(final_amount)
                # frappe.msgprint(final_amount)
                create_payment_entry(final_amount,razorpay_payment_link_reference_id,customer,razorpay_payment_link_id,actual_amount)
                return render_payment_success_page(final_amount,razorpay_payment_link_id)
                # You can now use this information as needed, such as updating your database, notifying users, etc.
            else:
                frappe.msgprint('Amount Paid not found in the response.')
                
        else:
            frappe.msgprint(f'Request failed with status code: {response.status_code}')
            frappe.msgprint(f'Response text: {response.text}')
    except Exception as e:
        frappe.msgprint(f'Error: {e}')


def render_payment_success_page(final_amount,razorpay_payment_link_id):
    # HTML template for the success page
    success_html = f"""
    <html>
        <head>
            <title>Payment Success!!!!</title>
            <style>
                .btn.btn-primary.btn-sm.btn-block {{
                    display: none !important;
                }}
                
            </style>
        </head>
        <body>
            <h1>Payment Successful</h1>
            <p>Transaction: {razorpay_payment_link_id}</p>
            <p>Amount: {final_amount}</p>
            <!-- Add any additional information you want to display -->
        </body>
    </html>
    """
    
    
    frappe.respond_as_web_page("Payment Success", success_html)






# @frappe.whitelist(allow_guest=True)
def create_payment_entry(final_amount, razorpay_payment_link_reference_id, customer, razorpay_payment_link_id, actual_amount):
    try:
        # print("actual_amount=", actual_amount)
        # print("customer=", customer)
        # print("razorpay_payment_link_reference_id=", razorpay_payment_link_reference_id)
        # print("===========")
        # print(f"User: {frappe.session.user}")
        # print(f"User Roles: {frappe.get_roles(frappe.session.user)}")
        frappe.set_user("Administrator")
        
        # Check if entry exists in the database. If yes, directly return.
        if is_payment_entry_exists(razorpay_payment_link_id):
            frappe.msgprint(_('Payment Entry already exists. Skipping creation.'))
            return
            
        # Create a Payment Entry
        payment_entry = frappe.get_doc({
            "doctype": "Payment Entry",
            "paid_from": "Debtors - IND",
            "paid_to": "Razorpay - IND",
            "received_amount": "INR",
            "base_received_amount": "INR",
            "paid_amount": int(final_amount),
            "references": [
                {
                    "reference_doctype": "Sales Order",
                    "reference_name": razorpay_payment_link_reference_id,
                    "allocated_amount": int(actual_amount)
                }
            ],
            "reference_date": today(),
            "account": "Accounts Receivable",
            "party_type": "Customer",
            "party": customer,
            "mode_of_payment": "Razorpay",
            "reference_no": razorpay_payment_link_id
        }, ignore_permissions=True)
        
        # print("=============STARTED=============")

        # Save the Payment Entry
        payment_entry.insert(ignore_permissions=True)
        frappe.db.commit()
        # print("=============ENDED=============")
        frappe.set_user("Guest")

    except frappe.exceptions.ValidationError as e:
        frappe.msgprint(_('Error creating Payment Entry: {0}').format(str(e)))

# Rest of your code...


def is_payment_entry_exists(reference_id):
    # Check if a Payment Entry with the given reference already exists
    # Replace with your actual logic to check if a Payment Entry exists
    # For example, you can use frappe.get_value to check if a record with the given reference exists
    existing_payment_entry = frappe.get_value("Payment Entry", {"reference_no": reference_id})

    return bool(existing_payment_entry)






##################################################################

# Gst monthly filling


# from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def fetch_gstfile_records():
    try:
        # Fetch records from Gstfile with filter gst_type = 'regular'
        records = frappe.get_all("Gstfile", filters={"gst_type": "regular"}, fields=["gst_number"])
        # frappe.msgprint(records)
        return records
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in fetch_gstfile_records")
        return None
    
    
##############################################################################

# IT Assessess Create manual Record


# from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def create_it_assessee_manual_record(yearly_report, current_form_name):
    try:
        # Your logic to create a new record in 'IT Assessee Filing Data'
        filing_data_doc = frappe.new_doc('IT Assessee Filing Data')
        filing_data_doc.ay = yearly_report
        filing_data_doc.it_assessee_file = current_form_name
        filing_data_doc.save()

        return True  # Return True if the operation is successful
    except Exception as e:
        frappe.log_error(f"Error in creating IT Assessee Filing Data: {str(e)}")
        return False  # Return False if there's an error
    
    
    
##############################################################################

# In sales order Fetch service from master




@frappe.whitelist()
def fetch_services(c_id=None):
    all_services = frappe.get_all("Customer Chargeable Doctypes")
    c_services=[]
    for service in all_services:
        # print(service["name"])
        # if service["name"] in ("IT Assessee File","Gstfile"):
            # print(service["name"])
        c_services_n= (frappe.get_all(
            service["name"], 
            filters={'customer_id': c_id,"enabled":1},
            fields=["name","service_name","hsn_code","description","customer_id","current_recurring_fees"]))
        c_services+=list(c_services_n)
            # for c_service in c_services_n:
            #   pass
    print(c_services)
    
    if c_services:
        # For demonstration purposes, let's just send back a response.
        data = c_services
        return data
    else:
        return "No data found for the given parameters."



#############################################################################################

import frappe
from datetime import datetime
import calendar
 
 
 
 
def cron():
    auto_gen_so_for_subscribers()
    # pass
    
        
 
        
        
def auto_gen_so_for_subscribers():
 
    subscriptions = frappe.get_all("Customer Subscriptions Plan",
    filters={"status":"Active"},
    fields=["name","customer_id","subscription_start_date","action_frequency","notification","whatsapp","email"])
 
    monthly_subscriptions=[i for i in subscriptions if i["action_frequency"]=="Monthly"]
 
    for subscriber in monthly_subscriptions:
        c_id=subscriber["customer_id"]
 
        current_date = datetime.now().date()
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        last_day_of_month = datetime(current_date.year, current_date.month, last_day)
 
        s_id=subscriber["name"]
        subscription_services = frappe.get_all("Subscription Item",
            filters={"parent":s_id},
            fields=["services_name","hsn_code","qty","rate"])
 
        items_list=[]
        qtyy=0
        amt=0.00
        for service in subscription_services:
            items_list+=[
                    {
                    "item_code": service["services_name"],
                    "gst_hsn_code": service["hsn_code"],
                    "qty": service["qty"],
                    "rate":service["rate"]
                    }
                    ]
            qtyy+=service["qty"]
            amt+=service["rate"]
     
 
        sales_order = frappe.get_doc({"doctype": "Sales Order", "customer": c_id,
        "transaction_date":current_date,"custom_so_from_date":current_date,
        "custom_so_to_date":last_day_of_month,"total_qty":qtyy,"total":amt,
        "items": items_list
        })
        sales_order.insert()
 
  
  
  
  ###############################################################################################
  
  # Issue to Task Creation


@frappe.whitelist()
def task_with_issue_creation(i_id=None):
    issue = frappe.get_last_doc("Issue", filters={"name": i_id})

    if not issue:
        return f"Issue {i_id} not found"

    issue_task = frappe.get_all("Task", filters={"issue": i_id})

    if issue_task:
        return f"Task already created for Issue {i_id}"

    task = frappe.get_doc({
        "doctype": "Task",
        "subject": issue.subject,
        "custom_customer_id": issue.customer,
        "priority": issue.priority,
        "issue": issue.name,
        "project": "PROJ-0019",
        "description": issue.description,
        "custom_task_type": issue.issue_type,
    })

    task.insert()

    print(issue.subject)

    return f"New Task created for Issue {i_id}"
    
    
    
###############################################################################################
  
# Aisensy integration for Sales Order Without Payment Link

@frappe.whitelist(allow_guest=True)
def aisensy_sales_order_wo_link(docname,customer_id, customer,from_date,to_date,total,new_mobile,advance_paid):
    try:
        amount_pending=float(total) - float(advance_paid)
        company_account_details="Template Awaited"
        # frappe.msgprint(from_date)
        # pass
        ai_sensy_api = frappe.get_doc('Ai Sensy Api')

        application_url = ai_sensy_api.application_url
        ai_sensy_url = ai_sensy_api.ai_sensy_url
        ai_sensy_api1 = ai_sensy_api.ai_sensy_api
        # Check if Sales Order exists
        if not frappe.get_value('Sales Order', docname):
            frappe.msgprint(_("Sales Order {0} not found.").format(docname))
            return

        # Fetch the Sales Order document
        # sales_invoice = frappe.get_doc('Sales Order', docname)
        # erpnext_url = application_url

        # Replace the following URL with the actual AI Sensy API endpoint
        sensy_api_url = ai_sensy_url

        sales_order_url = frappe.utils.get_url(
            f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Order&name={docname}&http://192.168.1.31:8028/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Order&name=SAL-ORD-2024-00000&format=Sales%20Order%20Format&no_letterhead=0&letterhead=360ithub&settings=%7B%7D&_lang=en"
        )
        # Example payload to send to the AI Sensy API
        payload = {
            "apiKey": ai_sensy_api1,  # Replace with your actual API key
            "campaignName": "lsa_saleorder_invoice",
            "destination": new_mobile,
            "userName": customer,
            "templateParams": [
                customer,
                from_date,
                to_date,
                # format_date(from_date, "dd-mmm-yyyy"),  # Format from_date
                # format_date(to_date, "dd-mmm-yyyy"),
                total,
                advance_paid,
                amount_pending,
                company_account_details,
            ],
            "media": {
                "url": sales_order_url,
                # "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "filename": docname
            }
        }

        # Make a POST request to the AI Sensy API
        response = requests.post(sensy_api_url, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Log the API response for reference
            frappe.logger().info(f"AI Sensy response: {response.text}")

            # You can update the Sales Invoice or perform other actions based on the API response
            # sales_invoice.custom_field = response.json().get('result')
            # sales_invoice.save()

            frappe.msgprint(_("WhatsApp Message Sent successfully : {0}").format(response.text))
            whatsapp_message_log = frappe.new_doc('WhatsApp Message Log')
            whatsapp_message_log.sales_order = docname
            whatsapp_message_log.customer = customer_id
            whatsapp_message_log.sender = frappe.session.user  # Add the sender information
            whatsapp_message_log.send_date = frappe.utils.now_datetime()
            # whatsapp_message_log.from_date = from_date
            # whatsapp_message_log.to_date = to_date
            whatsapp_message_log.total_amount = total
            whatsapp_message_log.mobile_no = new_mobile
            whatsapp_message_log.razorpay_payment_link = "Without Link"
            whatsapp_message_log.insert(ignore_permissions=True)
        else:
            # Log the error and provide feedback to the user
            frappe.logger().error(f"Sensy API Error: {response.text}")
            frappe.msgprint(_("WhatsApp message failed to send!. Please try again Later."))

    except requests.exceptions.RequestException as e:
        # Log the exception and provide feedback to the user
        print(e)
        frappe.logger().error(f"Network error: {e}")
        frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later.",e))

    except Exception as e:
        # Log the exception and provide feedback to the user
        print(e)
        frappe.logger().error(f"Custom Button Script Error: {e}")
        frappe.msgprint(_("An error occurred while WhatsApp Message. Please try again Later.",e))
    
    
    


@frappe.whitelist()
def share_lead_with_user(lead_name, user):
    frappe.share.add('Lead', lead_name, user, read=1, write=1)
    return "Success"
    
    
    


@frappe.whitelist()
def delete_all_data_import_logs():
    try:
        frappe.db.sql('DELETE FROM `tabData Import Log`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}



@frappe.whitelist()
def delete_all_data_import_logs_lead():
    try:
        frappe.db.sql('DELETE FROM `tabLead`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


@frappe.whitelist()
def delete_all_data_import_logs_Contact():
    try:
        frappe.db.sql('DELETE FROM `tabContact`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
        
        
        
        
@frappe.whitelist()
def delete_all_data_import_logs_Customer():
    try:
        frappe.db.sql('DELETE FROM `tabCustomer`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
        
        
        
        
        
        
        
       
@frappe.whitelist()
def create_todo(date, description, lead_name, lead_id, assign_to=None, category=None):
    todo = frappe.get_doc({
        'doctype': 'ToDo',
        'date': date,
        'allocated_to': assign_to,
        'description': description,
        'custom_category': category,
        'reference_type': "Lead",
        'reference_name': lead_id,
        'custom_lead_id1':lead_id,
        'custom_lead_name': lead_name
    })
    todo.insert(ignore_permissions=True)

    return todo.name


@frappe.whitelist()
def get_open_activities(lead_id):
    # Fetch open ToDos
    todos = frappe.get_all('Lead Follow Up', filters={'status': 'Open','lead_id':lead_id}, fields=['name', 'date', 'description','allocated_to','custom_category'])
    return todos
    
    
    
    
@frappe.whitelist()
def close_todo(todo_name):
    try:
        # Load the ToDo
        todo = frappe.get_doc('Lead Follow Up', todo_name)
        
        # Set the status to 'Closed'
        todo.status = 'Closed'
        
        # Save the changes
        todo.save()
        
        return True
    except frappe.DoesNotExistError:
        frappe.msgprint(f"ToDo {todo_name} not found.")
        return False
    except Exception as e:
        frappe.msgprint(f"Error closing ToDo: {str(e)}")
        return False
        
        
        
        
        
        
        
       
@frappe.whitelist()
def sync_lead_records():
    try:
        # Fetch all lead records
        lead_records = frappe.get_all('Lead', filters={'custom_assign_to': ('is', 'set')}, fields=['name', 'custom_assign_to'])

        # Share each lead record with custom_assign_to user
        for lead in lead_records:
            custom_assign_to = lead.get('custom_assign_to')

            if custom_assign_to:
                # Share the lead record with custom_assign_to user
                frappe.share.add('Lead', lead.name, custom_assign_to, read=1, write=1)

        return True
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _('Sync Lead Records Error'))
        return False
   
   
   
   
   
@frappe.whitelist()
def get_todo_details(todo_name):
    todo = frappe.get_doc('Lead Follow Up', todo_name)
    return {
        'description': todo.description,
        'custom_category': todo.custom_category,
        'date': todo.date,
        'allocated_to': todo.allocated_to
        # Add more fields as needed
    }     
    
    
    
    
@frappe.whitelist()
def update_todo(todo_name, updated_values):
    todo = frappe.get_doc('Lead Follow Up', todo_name)

    # Parse the JSON string into a dictionary
    updated_values_dict = frappe.parse_json(updated_values)

    # Update the ToDo with the edited values
    todo.update(updated_values_dict)
    todo.save()
    return True



import requests

@frappe.whitelist()
def send_whatsapp_message(docname, customer, customer_id, from_date,total, new_mobile):
    try:
        # Check if the mobile number has 10 digits
        if len(new_mobile) != 10:
            frappe.msgprint("Please provide a valid 10-digit mobile number.")
            return

        message = f'''Dear {customer},

Your Sale Order for {from_date}  is due for amount of Rs {total}/- Kindly pay on below bank amount details

Our Bank Account
Lokesh Sankhala and ASSOSCIATES
Account No = 73830200000526
IFSC = BARB0VJJCRO
Bank = Bank of Baroda,JC Road,Bangalore-560002
UPI id = LSABOB@UPI
Gpay / Phonepe no = 9513199200

Call us immediately in case of query.

Best Regards,
LSA Office Account Team
accounts@lsaoffice.com'''
        
        link = frappe.utils.get_url(
            f"/api/method/frappe.utils.print_format.download_pdf?doctype=Sales%20Order&name={docname}&format=Sales%20Order%20Format&no_letterhead=0&letterhead=360ithub&settings=%7B%7D&_lang=en/360ithub-{docname}.pdf"
        )



        url = "https://wts.vision360solutions.co.in/api/sendFileWithCaption"
        params = {
            "token": "609bc2d1392a635870527076",
            "phone": f"91{new_mobile}",
            "message": message,
            "link": link
        }
        response = requests.post(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP errors (status codes other than 2xx)
        response_data = response.json()

        # # Check if the response status is 'success'
        # if response_data.get('status') == 'success':
        #     # Log the success
        #     frappe.logger().info("WhatsApp message sent successfully")


        frappe.logger().info(f"Sales Invoice response: {response.text}")

        # Create a new WhatsApp Message Log document
        sales_invoice_whatsapp_log = frappe.new_doc('WhatsApp Message Log')
        sales_invoice_whatsapp_log.sales_order = docname
        sales_invoice_whatsapp_log.customer = customer_id
        sales_invoice_whatsapp_log.posting_date = from_date
        sales_invoice_whatsapp_log.send_date = frappe.utils.nowdate() 
        sales_invoice_whatsapp_log.total_amount = total
        sales_invoice_whatsapp_log.mobile_no = new_mobile
        sales_invoice_whatsapp_log.sales_order = docname
        sales_invoice_whatsapp_log.sender = frappe.session.user 
        sales_invoice_whatsapp_log.insert(ignore_permissions=True)
        frappe.msgprint("WhatsApp message sent successfully")

    except requests.exceptions.RequestException as e:
        # Log the exception and provide feedback to the user
        frappe.logger().error(f"Network error: {e}")
        frappe.msgprint("An error occurred while sending the WhatsApp message. Please try again later.")

    except Exception as e:
        # Log the exception and provide feedback to the user
        frappe.logger().error(f"Error: {e}")
        frappe.msgprint("An unexpected error occurred while sending the WhatsApp message. Please contact the system administrator.")
    


import frappe
import requests
from frappe import _
from frappe.utils import today
from datetime import datetime



@frappe.whitelist()
def sync_sales_orders_followup(so_id=None):
    try:
        
        followup_values={"values":[],}
        if so_id:
            existing_followups=frappe.get_all("Customer Followup",
                                    fields=["name","sales_order_summary"])
            existing_so_followups=[i.name for i in existing_followups if so_id in i.sales_order_summary]
            # print(existing_sales_orders)
            if existing_so_followups:
                for existing_so_followup in existing_so_followups:
                    # print(existing_sales_order)
                    followup=frappe.get_doc("Customer Followup",existing_so_followup)


                    followup_values["values"]+=[[followup.customer_id,followup.name,
                                                followup.status,followup.total_remaining_balance,
                                                followup.followup_date,followup.next_followup_date,
                                                followup.executive_name,followup.followup_note]]
            #############################################################################################
            existing_payments=frappe.get_all("Payment Entry Reference",
                                              filters={"reference_name":so_id,"docstatus":1},
                                                fields=["name","creation","parent","total_amount","outstanding_amount",
                                                        "allocated_amount"])

            
            so_doc=frappe.get_doc("Sales Order",so_id)
            so_balance=so_doc.rounded_total
            payment_status = "Unpaid"
            existing_payments_list=[]
            for existing_payment in existing_payments:

                reference_date=''
                mode_of_payment=''
                existing_payment_entry=frappe.get_all("Payment Entry",
                                              filters={"name":existing_payment.parent},
                                                fields=["name","reference_date","paid_to"])
                reference_date=existing_payment_entry[0].reference_date
                mode_of_payment=existing_payment_entry[0].paid_to

                existing_payment_list=[existing_payment.parent,
                                       existing_payment.allocated_amount,reference_date,mode_of_payment]
                so_balance-=existing_payment.allocated_amount
                existing_payments_list.append(existing_payment_list)


            if so_balance == 0:
                payment_status = "Cleared"
            elif so_doc.rounded_total>so_balance > 0:
                payment_status = "Partially Paid"
            # print(existing_payments_list)
            return {"status":"Synced successfully.","followup_values":followup_values,"payment_values":existing_payments_list,"so_balance":so_balance,"payment_status":payment_status}
        # else:
        #     return {"status":"Synced successfully."}
    except Exception as e:
        frappe.msgprint(f"Error: {e}")
        return False


@frappe.whitelist()
def whatsapp_button(user_email=None):
    try:
        status = False
        user_roles = frappe.get_all('Has Role', filters={'parent': user_email}, fields=['role'])

        if user_email=="pankajsankhla90@gmail.com":
            user_roles = frappe.get_all('Has Role', filters={'parent': "Administrator"}, fields=['role'])

        # Extract roles from the result
        roles = [role.get('role') for role in user_roles]
        doc_perm_roles = ["LSA Accounts Manager","LSA Account Executive"]

        for role in roles:
            if role in doc_perm_roles:
                status = True
                break

        return {"status": status, "value": [roles]}

    except Exception as e:
        #print(e)
        return {"status": "Failed"}


@frappe.whitelist()
def gst_tax_type(customer_id=None):
    if customer_id:
        try:
            # gst_tax_type=""
            comp_gst_state=frappe.get_all("Company",fields=["custom_state"])
            
            cust_gst_state=frappe.get_all("Customer",fields=["custom_state"],filters={"name":customer_id})

            if comp_gst_state and cust_gst_state:

                comp_gst_state=comp_gst_state[0].custom_state
                cust_gst_state=cust_gst_state[0].custom_state
                if comp_gst_state==cust_gst_state:
                    gst_tax_type="Output GST In-state - IND"
                else:
                    gst_tax_type="Output GST In-state - IND"
        
                return {"status":True,"gst_tax_type":gst_tax_type}
        except Exception as er:
            return {"status":True,"error":er}


