#!/usr/bin/env python3
"""GitHub Contributions Checker - Simple Version"""
import subprocess, sys
from datetime import datetime

def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30).stdout.strip()
    except:
        return ""

# Track requirements
checks_passed = []
checks_failed = []

print("="*70)
print("   GITHUB CONTRIBUTIONS DIAGNOSTIC")
print("="*70)

# Email
print("\n1. EMAIL CONFIGURATION")
print("-"*70)
email = run("git config user.email")
print(f"   Git email: {email}")
if email:
    print("   ✅ Email configured")
    print(f"   ⚠️  Must be VERIFIED at: https://github.com/settings/emails")
    checks_passed.append("Email configured in git")
else:
    print("   ❌ No email configured!")
    print("   Fix: git config --global user.email 'your@email.com'")
    checks_failed.append("Email not configured")

# Branch
print("\n2. BRANCH CHECK")
print("-"*70)
current = run("git branch --show-current")
default = run("git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'") or "main"
print(f"   Current branch: {current}")
print(f"   Default branch: {default}")
if current == default:
    print("   ✅ On default branch (contributions will count)")
    checks_passed.append("On default branch")
else:
    print(f"   ❌ NOT on default branch!")
    print(f"   Fix: git checkout {default}")
    checks_failed.append("Not on default branch")

# Commits
print("\n3. RECENT COMMITS")
print("-"*70)
commits = run('git log --pretty=format:"%h|%ae|%ad" --date=short -5')
if commits:
    # Check if commit emails match configured email
    commit_emails = set()
    for line in commits.split('\n'):
        if '|' in line:
            h,e,d = line.split('|')
            commit_emails.add(e)
            print(f"   {h[:7]} {e[:30]:<30} {d}")
    
    if email in commit_emails:
        print(f"   ✅ Commits use configured email ({email})")
        checks_passed.append("Commits use correct email")
    else:
        print(f"   ⚠️  Some commits use different email!")
        print(f"   Configured: {email}")
        print(f"   In commits: {', '.join(commit_emails)}")
    
    print("   ⚠️  Email MUST be verified in GitHub!")
    checks_passed.append("Commits exist")
else:
    print("   ❌ No commits found")
    checks_failed.append("No commits in repository")

# Remote
print("\n4. REMOTE REPOSITORY")
print("-"*70)
remote = run("git remote get-url origin")
username = ""
if "github.com/" in remote:
    username = remote.split("github.com/")[1].split("/")[0]
elif "github.com:" in remote:
    username = remote.split("github.com:")[1].split("/")[0]
print(f"   Remote URL: {remote}")

if "github.com" in remote:
    print("   ✅ GitHub repository")
    checks_passed.append("Repository is on GitHub")
else:
    print("   ❌ Not a GitHub repository!")
    checks_failed.append("Not a GitHub repository")

if username:
    print(f"   GitHub Profile: https://github.com/{username}")
    print(f"   Email Settings: https://github.com/settings/emails")
    print(f"   Privacy Settings: https://github.com/settings/profile")

# Check if pushed
local_hash = run("git rev-parse HEAD")
remote_hash = run("git rev-parse @{u} 2>/dev/null")

if local_hash and remote_hash:
    if local_hash == remote_hash:
        print("   ✅ Local and remote in sync (pushed)")
        checks_passed.append("Changes pushed to GitHub")
    else:
        print("   ⚠️  Local ahead of remote - need to push!")
        checks_failed.append("Changes not pushed yet")
else:
    print("   ⚠️  Cannot verify push status")

# Stats
print("\n5. COMMIT STATISTICS")
print("-"*70)
year = datetime.now().year - 1
total = run(f'git log --since="{year}-01-01" --oneline | wc -l')
today = run(f'git log --since="{datetime.now().strftime("%Y-%m-%d")}" --oneline | wc -l')

print(f"   Commits since {year}: {total}")
print(f"   Commits today: {today}")

if total and int(total.strip()) > 0:
    print(f"   ✅ Repository has {total} commits")
else:
    print("   ⚠️  Very few commits found")

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
print("   VERIFICATION STATUS")
print("="*70)

total_checks = len(checks_passed) + len(checks_failed)
passed_count = len(checks_passed)

print(f"\n✅ PASSED ({passed_count} checks):")
for check in checks_passed:
    print(f"   ✓ {check}")

if checks_failed:
    print(f"\n❌ FAILED ({len(checks_failed)} checks):")
    for check in checks_failed:
        print(f"   ✗ {check}")

print(f"\n📊 SCORE: {passed_count}/{total_checks} checks passed")

# Final verdict
print("\n" + "="*70)
if len(checks_failed) == 0:
    print("   ✅ ALL AUTOMATED CHECKS PASSED!")
    print("="*70)
    print("\n🎉 Good news! All automated checks passed.")
    print("\n⚠️  However, you MUST manually verify:")
    print(f"   1. Email '{email}' is VERIFIED at:")
    print("      → https://github.com/settings/emails")
    print("      → Must have green checkmark ✓")
    print("\n   2. If repository is PRIVATE, enable:")
    print("      → https://github.com/settings/profile")
    print("      → Check ☑️ 'Include private contributions'")
    print("\n   3. Wait 24-48 hours for stats to fully update")
    print("      → Graph updates: 5-30 minutes")
    print("      → Total stats: 24-48 HOURS")
else:
    print("   ⚠️  SOME CHECKS FAILED - ACTION REQUIRED!")
    print("="*70)
    print("\n❌ Please fix the issues above first.")
    print("   Run this script again after making changes.")

print("\n" + "="*70)
print("   MANUAL CHECKLIST")
print("="*70)
print("  ☐ Email is VERIFIED in GitHub (check manually!)")
print("  ☐ On DEFAULT branch (main/master)")  
print("  ☐ 'Include private contributions' ON (if private repo)")
print("  ☐ Waited 24-48 hours for stats update")
print("="*70)

# Summary
print("\n💡 Quick Summary:")
if len(checks_failed) == 0:
    print("   → All automated checks passed ✅")
    print("   → Verify email manually in GitHub ⚠️")
    print("   → Wait 24-48 hours for stats ⏰")
else:
    print(f"   → Fix {len(checks_failed)} issue(s) above ❌")
    print("   → Then run this script again 🔄")

print("\n" + "="*70)
