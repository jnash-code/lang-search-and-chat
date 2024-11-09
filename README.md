คำตอบเอามาจาก
https://www.reddit.com/r/git/comments/ypnys6/i_want_to_revert_the_code_to_a_previous_commit/


1. git checkout -f HEAD~16 -- . will make your code go back 16 commits in your local storage, without rewriting any history with those 16 commits. The "changes" (reverting the past 16 commits) should be at the staging area at this moment.

2. Now you can git commit to commit those reverted code and then git push to update your Github repo.

3. To be sure you did it right, try git diff HEAD..HEAD~17 to compare your branch to the branch 17 commits ago (the 16 commits you wanted to revert + the new commit that did the revert = 17 commits). If the command outputs nothing, you're all good.

รัน git ใน TERMINAL: bash ด้านล่าง