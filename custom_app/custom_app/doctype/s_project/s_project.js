// Copyright (c) 2024, pankaj@360ithub.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("S Project", {
	setup(frm) {
		frm.make_methods = {
			'Timesheet': () => {
				open_form(frm, "S Timesheet", "S Timesheet Detail", "time_logs");
			},
			
		};
	},
	onload: function (frm) {
		const so = frm.get_docfield("sales_order");
		so.get_route_options_for_new_doc = () => {
			if (frm.is_new()) return {};
			return {
				"customer": frm.doc.customer,
				"project_name": frm.doc.name
			};
		};

		frm.set_query('customer', 'erpnext.controllers.queries.customer_query');

		// frm.set_query("user", "users", function () {
		// 	return {
		// 		query: "custom_app.custom_app.doctype.s_project.s_project.get_users_for_project"
		// 	};
		// });

		// sales order
		frm.set_query('sales_order', function () {
			var filters = {
				'project': ["in", frm.doc.__islocal ? [""] : [frm.doc.name, ""]]
			};

			if (frm.doc.customer) {
				filters["customer"] = frm.doc.customer;
			}

			return {
				filters: filters
			};
		});
	},

	refresh: function (frm) {
		if (frm.doc.__islocal) {
			frm.web_link && frm.web_link.remove();
		} else {
			frm.add_web_link("/projects?project=" + encodeURIComponent(frm.doc.name));

			frm.trigger('show_dashboard');
		}
		frm.trigger("set_custom_buttons");
	},

	set_custom_buttons: function(frm) {
		if (!frm.is_new()) {
			// frm.add_custom_button(__('Duplicate Project with Tasks'), () => {
			// 	frm.events.create_duplicate(frm);
			// }, __("Actions"));

			// frm.add_custom_button(__('Update Total Purchase Cost'), () => {
			// 	frm.events.update_total_purchase_cost(frm);
			// }, __("Actions"));
			frm.add_custom_button(__('Create Task'), () => {
				createTask(frm);
			}, __("Actions"));

			frm.add_custom_button(__('Open Task'), () => {
				opentask(frm);
			}, __("Actions"));
			
			frm.add_custom_button(__('Open Timesheet'), () => {
				frappe.set_route('List', 'S Timesheet');
			}, __("Actions"));

			// frm.trigger("set_project_status_button");


			// if (frappe.model.can_read("S Task")) {
			// 	frm.add_custom_button(__("Gantt Chart"), function () {
			// 		frappe.route_options = {
			// 			"project": frm.doc.name
			// 		};
			// 		frappe.set_route("List", "S Task", "Gantt");
			// 	}, __("View"));

			// 	frm.add_custom_button(__("Kanban Board"), () => {
			// 		frappe.call('custom_app.custom_app.doctype.s_project.s_project.create_kanban_board_if_not_exists', {
			// 			project: frm.doc.name
			// 		}).then(() => {
			// 			frappe.set_route('List', 'S Task', 'Kanban', frm.doc.project_name);
			// 		});
			// 	}, __("View"));
			// }
		}


	},

	update_total_purchase_cost: function(frm) {
		frappe.call({
			method: "erpnext.projects.doctype.project.project.recalculate_project_total_purchase_cost",
			args: {project: frm.doc.name},
			freeze: true,
			freeze_message: __('Recalculating Purchase Cost against this Project...'),
			callback: function(r) {
				if (r && !r.exc) {
					frappe.msgprint(__('Total Purchase Cost has been updated'));
					frm.refresh();
				}
			}

		});
	},

	set_project_status_button: function(frm) {
		frm.add_custom_button(__('Set Project Status'), () => {
			let d = new frappe.ui.Dialog({
				"title": __("Set Project Status"),
				"fields": [
					{
						"fieldname": "status",
						"fieldtype": "Select",
						"label": "Status",
						"reqd": 1,
						"options": "Completed\nCancelled",
					},
				],
				primary_action: function() {
					frm.events.set_status(frm, d.get_values().status);
					d.hide();
				},
				primary_action_label: __("Set Project Status")
			}).show();
		}, __("Actions"));
	},

	create_duplicate: function(frm) {
		return new Promise(resolve => {
			frappe.prompt('Project Name', (data) => {
				frappe.xcall('custom_app.custom_app.doctype.s_project.s_project.create_duplicate_project',
					{
						prev_doc: frm.doc,
						project_name: data.value
					}).then(() => {
					frappe.set_route('Form', "Project", data.value);
					frappe.show_alert(__("Duplicate project has been created"));
				});
				resolve();
			});
		});
	},

	set_status: function(frm, status) {
		frappe.confirm(__('Set Project and all Tasks to status {0}?', [status.bold()]), () => {
			frappe.xcall('erpnext.projects.doctype.project.project.set_project_status',
				{project: frm.doc.name, status: status}).then(() => {
				frm.reload_doc();
			});
		});
	},

});

function open_form(frm, doctype, child_doctype, parentfield) {
	frappe.model.with_doctype(doctype, () => {
		let new_doc = frappe.model.get_new_doc(doctype);

		// add a new row and set the project
		let new_child_doc = frappe.model.get_new_doc(child_doctype);
		new_child_doc.project = frm.doc.name;
		new_child_doc.parent = new_doc.name;
		new_child_doc.parentfield = parentfield;
		new_child_doc.parenttype = doctype;
		new_doc[parentfield] = [new_child_doc];
		new_doc.project = frm.doc.name;

		frappe.ui.form.make_quick_entry(doctype, null, null, new_doc);
	});

}


function createTask(frm) {
    var project_code = frm.doc.name;

    // Open a new S Task form with the project code pre-filled
    frappe.new_doc('S Task', {
        project: project_code
        // Add other fields to pre-fill as needed
    });
}


function opentask(frm){
	    if (frm.doc.name) {
        // Construct the URL for the Todo List with the Lead name
        var projectname = frm.doc.name;
        var baseUrl = 'http://erp.360ithub.com/app/';
        var url = baseUrl + 's-task?project=' + projectname;

        // Open the Todo List in a new tab or window
        window.open(url, '_blank');
    } else {
        frappe.msgprint(__('Task does not have a name.'));
    }
}
