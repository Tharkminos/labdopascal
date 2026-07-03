#!/bin/bash
git add .
commit='user'
echo "Escreva seu commit"
read commit 
echo "Commit: $commit gerado!"
git commit -m "$commit" || exit 1
git push https://Tharkminos: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@github.com/Tharkminos/labdopascal
