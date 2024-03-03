import frappe

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
    
