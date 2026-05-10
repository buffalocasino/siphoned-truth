#!/bin/bash
# Test dispatch - spawn a simple one-shot task
hermes kanban dispatch \
  --profile scribe \
  --skills kanban-worker \
  --one-shot \
  --timeout 120 \
  "echo 'Kanban dispatch works' && kanban_complete(summary='test passed')" \
  "Test: echo hello and complete" 2>&1
