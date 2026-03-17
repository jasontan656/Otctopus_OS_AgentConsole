cd __REPO_ROOT__
export TMPDIR=__TMP_DIR__
export TMP=__TMP_DIR__
export TEMP=__TMP_DIR__
codex exec --json --ephemeral --dangerously-bypass-approvals-and-sandbox -C __REPO_ROOT__ -m gpt-5.4 -c 'model_reasoning_effort="high"' -o __LAST_MESSAGE_PATH__ - < __PROMPT_PATH__ > __LOG_PATH__ 2>&1
rc=$?
printf "%s\n" "$rc" > __EXIT_CODE_PATH__
if [ "$rc" -eq 0 ]; then
  printf "done\n" > __STATE_PATH__
else
  printf "failed\n" > __STATE_PATH__
fi
exec bash
