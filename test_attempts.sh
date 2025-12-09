#!/usr/bin/env bash
# Run this after starting uvicorn (app:app) at http://127.0.0.1:8000
# Usage: bash test_attempts.sh

BASE="http://127.0.0.1:8000"
hdr=(-H "Content-Type: application/json")

echo "1) Single wrong attempt (baseline)"
curl -sS "${BASE}/attempt" "${hdr[@]}" -d '{
  "student_id":"student_w1",
  "question_id":"q1",
  "topic":"algebra/linear-equations",
  "difficulty":"easy",
  "correct":false,
  "time_spent_seconds":40
}' | python -m json.tool
echo
sleep 0.4

echo "2) Second wrong attempt -> should trigger decrease_difficulty (wrong streak of 2)"
curl -sS "${BASE}/attempt" "${hdr[@]}" -d '{
  "student_id":"student_w1",
  "question_id":"q1",
  "topic":"algebra/linear-equations",
  "difficulty":"easy",
  "correct":false,
  "time_spent_seconds":30
}' | python -m json.tool
echo
sleep 0.4

echo "3) Three correct attempts to another student -> should trigger increase_difficulty"
for i in 1 2 3; do
  curl -sS "${BASE}/attempt" "${hdr[@]}" -d "{
    \"student_id\":\"student_c1\",
    \"question_id\":\"q1\",
    \"topic\":\"algebra/linear-equations\",
    \"difficulty\":\"easy\",
    \"correct\":true,
    \"time_spent_seconds\":25
  }" | python -m json.tool
  echo
  sleep 0.3
done

echo "4) Multiple fails to mark topic as weak and get a micro-lesson (student_weak1)"
curl -sS "${BASE}/attempt" "${hdr[@]}" -d '{
  "student_id":"student_weak1",
  "question_id":"q4",
  "topic":"algebra/inequalities",
  "difficulty":"easy",
  "correct":false,
  "time_spent_seconds":50
}' | python -m json.tool
echo
sleep 0.3

curl -sS "${BASE}/attempt" "${hdr[@]}" -d '{
  "student_id":"student_weak1",
  "question_id":"q4",
  "topic":"algebra/inequalities",
  "difficulty":"easy",
  "correct":false,
  "time_spent_seconds":35
}' | python -m json.tool
echo
sleep 0.3

curl -sS "${BASE}/attempt" "${hdr[@]}" -d '{
  "student_id":"student_weak1",
  "question_id":"q4",
  "topic":"algebra/inequalities",
  "difficulty":"easy",
  "correct":false,
  "time_spent_seconds":40
}' | python -m json.tool
echo
sleep 0.3

echo "Done. If you want more sequences, copy/paste and change student_id/topic/difficulty/correct."
