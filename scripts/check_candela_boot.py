import frappe

def run():
    frappe.init(site="dev.localhost")
    frappe.connect()
    frappe.set_user("Administrator")
    
    from frappe.boot import load_desktop_data
    
    class BI(dict):
        def __getattr__(self, key):
            return self.get(key)
        def __setattr__(self, key, val):
            self[key] = val
    
    frappe.cache.delete_keys("desktop_icons")
    frappe.cache.delete_keys("bootinfo")
    
    bi = BI()
    load_desktop_data(bi)
    
    ad = bi.get("app_data", [])
    print(f"Total app_data entries: {len(ad)}")
    
    for app in ad:
        n = app.get("app_name", "")
        t = app.get("app_title", "")
        r = app.get("app_route", "")
        ws = app.get("workspaces", [])
        print(f"  {n:20s} title={t:30s} route={r:30s} ws={ws}")
    
    print()
    candela = [a for a in ad if a.get("app_name") == "candela"]
    if candela:
        print("✅ Candela FOUND in app_data!")
        print(f"   Details: {candela[0]}")
    else:
        print("❌ Candela NOT FOUND in app_data!")
    
    frappe.destroy()

if __name__ == "__main__":
    run()
