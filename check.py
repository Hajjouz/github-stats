#!/usr/bin/env python3
"""GitHub Contributions Checker - Simple Version"""
import subprocess, sys
from datetime import datetime

def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except:
        return ""

print("="*70)
print("   GITHUB CONTRIBUTIONS DIAGNOSTIC")
print("="*70)

# Email
print("\n1. EMAIL")
print("-"*70)
email = run("git config user.email")
print(f"   Git email: {email}")
if email:
    print("   ✅ Configured")
    print(f"   ⚠️  VERIFY at: https://github.com/settings/emails")
else:
    print("   ❌ No email! Fix: git config --global user.email 'your@email.com'")

# Branch
print("\n2. BRANCH")
print("-"*70)
current = run("git branch --show-current")
default = run("git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'") or "main"
print(f"   Current: {current} | Default: {default}")
if current == default:
    print("   ✅ On default branch")
else:
    print(f"   ❌ Not on default! Fix: git checkout {default}")

# Commits
print("\n3. RECENT COMMITS")
print("-"*70)
commits = run('git log --pretty=format:"%h|%ae|%ad" --date=short -5')
if commits:
    for line in commits.split('\n'):
        if '|' in line:
            h,e,d = line.split('|')
            print(f"   {h[:7]} {e[:30]:<30} {d}")
    print("   ⚠️  Email must match GitHub verified email!")
else:
    print("   ❌ No commits")

# Remote
print("\n4. REMOTE")
print("-"*70)
remote = run("git remote get-url origin")
username = ""
if "github.com/" in remote:
    username = remote.split("github.com/")[1].split("/")[0]
elif "github.com:" in remote:
    username = remote.split("github.com:")[1].split("/")[0]
print(f"   URL: {remote}")
if username:
    print(f"   Profile: https://github.com/{username}")

# Stats
print("\n5. STATISTICS")
print("-"*70)
year = datetime.now().year - 1
total = run(f'git log --since="{year}-01-01" --oneline | wc -l')
print(f"   Commits since {year}: {total}")

# Solutions
print("\n" + "="*70)
print("   SOLUTIONS")
print("="*70)
print("""
📧 EMAIL NOT VERIFIED (90% of issues!)
   → https://github.com/settings/emails
   → Must have green checkmark ✓

🌳 NOT ON DEFAULT BRANCH
   → git checkout {0}
   → git push origin {0}

🔒 PRIVATE REPO
   → https://github.com/settings/profile
   → Check ☑️ 'Include private contributions'

⏰ WAIT 24-48 HOURS
   → Graph updates fast
   → Total stats update SLOW (24-48h)

🔄 FORCE REFRESH
   → git commit --allow-empty -m "Refresh"
   → git push
""".format(default))

print("="*70)
print("  CHECKLIST:")
print("  ☐ Email VERIFIED in GitHub")
print("  ☐ On DEFAULT branch")  
print("  ☐ 'Include private' ON")
print("  ☐ Waited 24-48 hours")
print("="*70)
