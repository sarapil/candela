// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT
// For license information, please see license.txt

/**
 * Candela User Management — CAPS visual interface
 * Manages roles, jobs, permissions from a single visual screen
 */
(function(){
	"use strict";
	const AMBER = "#F59E0B", DARK = "#1C1917";
	const ROLES = [
		"Candela Manager","Candela Staff","Candela Chef",
		"Candela Cashier","Candela Waiter","Candela Procurement","Candela Marketing"
	];

	window.candela = window.candela || {};
	window.candela.users = {
		init(selector){
			const container = document.querySelector(selector);
			if(!container) return;
			container.innerHTML = `
				<style>
					.cd-um{padding:24px;color:#D6D3D1;font-family:var(--cd-font-body,Inter,sans-serif)}
					.cd-um h2{color:${AMBER};margin:0 0 20px;font-size:1.5rem}
					.cd-um-grid{display:grid;grid-template-columns:300px 1fr;gap:20px;min-height:500px}
					.cd-um-list{background:rgba(28,25,23,.8);border:1px solid rgba(245,158,11,.15);border-radius:12px;padding:16px;overflow-y:auto;max-height:70vh}
					.cd-um-detail{background:rgba(28,25,23,.8);border:1px solid rgba(245,158,11,.15);border-radius:12px;padding:24px}
					.cd-um-item{padding:10px 12px;border-radius:8px;cursor:pointer;margin-bottom:4px;display:flex;align-items:center;gap:10px;transition:background .2s}
					.cd-um-item:hover,.cd-um-item.active{background:rgba(245,158,11,.12)}
					.cd-um-avatar{width:36px;height:36px;border-radius:50%;background:${AMBER};color:${DARK};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9rem}
					.cd-um-name{font-weight:600;color:#FEF3C7;font-size:.9rem}
					.cd-um-email{font-size:.8rem;color:#A8A29E}
					.cd-um-search{width:100%;padding:8px 12px;border-radius:8px;border:1px solid rgba(245,158,11,.2);background:rgba(0,0,0,.3);color:#FEF3C7;margin-bottom:12px;font-size:.9rem}
					.cd-um-search::placeholder{color:#78716C}
					.cd-um-roles{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
					.cd-um-role{padding:6px 14px;border-radius:20px;font-size:.82rem;font-weight:600;cursor:pointer;transition:all .2s;border:2px solid}
					.cd-um-role.on{background:${AMBER};color:${DARK};border-color:${AMBER}}
					.cd-um-role.off{background:transparent;color:#A8A29E;border-color:rgba(245,158,11,.2)}
					.cd-um-role.off:hover{border-color:${AMBER};color:${AMBER}}
					.cd-um-section{margin-top:20px}
					.cd-um-section h4{color:${AMBER};font-size:1rem;margin-bottom:8px}
					.cd-um-caps{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:6px}
					.cd-um-cap{padding:6px 10px;font-size:.8rem;background:rgba(245,158,11,.06);border-radius:6px;color:#D6D3D1;border:1px solid rgba(245,158,11,.1)}
					.cd-um-btn{background:${AMBER};color:${DARK};border:none;padding:8px 20px;border-radius:8px;font-weight:700;cursor:pointer;font-size:.9rem;margin-top:16px}
					.cd-um-btn:hover{filter:brightness(1.1)}
					.cd-um-perm-map{height:280px;border-radius:10px;overflow:hidden;margin-top:12px;background:${DARK}}
					@media(max-width:768px){.cd-um-grid{grid-template-columns:1fr}}
				</style>
				<div class="cd-um">
					<h2>👥 ${__("User Management")}</h2>
					<div class="cd-um-grid">
						<div class="cd-um-list">
							<input class="cd-um-search" placeholder="${__("Search users...")}" />
							<div class="cd-um-items"></div>
						</div>
						<div class="cd-um-detail">
							<p style="text-align:center;color:#78716C;padding:40px">${__("Select a user from the list")}</p>
						</div>
					</div>
				</div>`;

			this.container = container;
			this.loadUsers();
			container.querySelector(".cd-um-search").addEventListener("input", (e) => this.filterUsers(e.target.value));
		},

		async loadUsers(){
			const resp = await frappe.call({ method: "frappe.client.get_list", args: {
				doctype: "User", filters: { user_type: "System User", enabled: 1 },
				fields: ["name","full_name","email","user_image"], limit_page_length: 200
			}});
			this.users = (resp.message || []).filter(u => u.name !== "Administrator" && u.name !== "Guest");
			this.renderList(this.users);
		},

		renderList(users){
			const wrap = this.container.querySelector(".cd-um-items");
			wrap.innerHTML = users.map(u => `
				<div class="cd-um-item" data-user="${u.name}">
					<div class="cd-um-avatar">${(u.full_name || u.name).charAt(0).toUpperCase()}</div>
					<div><div class="cd-um-name">${u.full_name || u.name}</div><div class="cd-um-email">${u.email || u.name}</div></div>
				</div>`).join("");
			wrap.querySelectorAll(".cd-um-item").forEach(el => {
				el.addEventListener("click", () => this.selectUser(el.dataset.user));
			});
		},

		filterUsers(q){
			q = q.toLowerCase();
			const filtered = this.users.filter(u => (u.full_name || "").toLowerCase().includes(q) || u.name.toLowerCase().includes(q));
			this.renderList(filtered);
		},

		async selectUser(userId){
			// Highlight
			this.container.querySelectorAll(".cd-um-item").forEach(el => el.classList.toggle("active", el.dataset.user === userId));
			// Load user roles
			const resp = await frappe.call({ method: "frappe.client.get", args: { doctype: "User", name: userId }});
			const user = resp.message;
			const detail = this.container.querySelector(".cd-um-detail");
			const userRoles = (user.roles || []).map(r => r.role);

			detail.innerHTML = `
				<h3 style="color:#FEF3C7;margin:0 0 4px">${user.full_name || user.name}</h3>
				<p style="color:#A8A29E;font-size:.85rem;margin:0 0 16px">${user.email}</p>
				<div class="cd-um-section">
					<h4>🔑 ${__("Candela Roles")}</h4>
					<div class="cd-um-roles">
						${ROLES.map(r => `<span class="cd-um-role ${userRoles.includes(r)?'on':'off'}" data-role="${r}">${r.replace("Candela ","")}</span>`).join("")}
					</div>
				</div>
				<div class="cd-um-section">
					<h4>🛡️ ${__("Active Capabilities")}</h4>
					<div class="cd-um-caps" id="cd-um-caps"></div>
				</div>
				<div class="cd-um-section">
					<h4>🔗 ${__("Permission Map")}</h4>
					<div class="cd-um-perm-map" id="cd-um-perm-map"></div>
				</div>`;

			// Toggle roles
			detail.querySelectorAll(".cd-um-role").forEach(el => {
				el.addEventListener("click", async () => {
					const role = el.dataset.role;
					const isOn = el.classList.contains("on");
					try {
						if(isOn) {
							await frappe.call({ method: "frappe.client.delete", args: {
								doctype: "Has Role", name: (user.roles || []).find(r => r.role === role)?.name
							}});
						} else {
							await frappe.call({ method: "frappe.client.insert", args: {
								doc: { doctype: "Has Role", parent: userId, parenttype: "User", parentfield: "roles", role: role }
							}});
						}
						el.classList.toggle("on");
						el.classList.toggle("off");
						frappe.show_alert({ message: isOn ? __("Removed {0}", [role]) : __("Added {0}", [role]), indicator: isOn ? "orange" : "green" });
					} catch(e) {
						frappe.msgprint(__("Error updating role: {0}", [e.message || e]));
					}
				});
			});

			// Show capabilities from CAPS
			this.loadCapabilities(userRoles);

			// Render permission graph
			const mapEl = detail.querySelector("#cd-um-perm-map");
			if(mapEl && frappe.visual && frappe.visual.dependencyGraph){
				const nodes = [{ id: "user", label: user.full_name || userId, icon: "user" }];
				const edges = [];
				userRoles.filter(r => r.startsWith("Candela")).forEach(r => {
					const rid = r.replace(/ /g,"_");
					nodes.push({ id: rid, label: r.replace("Candela ",""), icon: "shield" });
					edges.push({ source: "user", target: rid });
				});
				frappe.visual.dependencyGraph({ container: mapEl, nodes, edges, theme: "dark" });
			}
		},

		async loadCapabilities(roles){
			const capsEl = this.container.querySelector("#cd-um-caps");
			if(!capsEl) return;
			try {
				const resp = await frappe.call({ method: "frappe.client.get_list", args: {
					doctype: "Role Capability Map", filters: { role: ["in", roles] },
					fields: ["capability"], limit_page_length: 200
				}});
				const caps = [...new Set((resp.message || []).map(c => c.capability))];
				capsEl.innerHTML = caps.length
					? caps.map(c => `<div class="cd-um-cap">${c}</div>`).join("")
					: `<p style="color:#78716C;font-size:.85rem">${__("No CAPS capabilities assigned")}</p>`;
			} catch(e){
				capsEl.innerHTML = `<p style="color:#78716C;font-size:.85rem">${__("CAPS not available")}</p>`;
			}
		}
	};
})();
