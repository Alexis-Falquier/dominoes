#!/bin/bash

# make test directory and copy api index to it
mkdir -p src/test
cp src/index.ts src/test/indexTest.ts

# correct relative file paths and substitute port 8000 for 8001
sed -i 's/\.\/blockchain/\.\.\/blockchain/g' src/test/indexTest.ts
sed -i 's/\.\/types\/custom/\.\.\/types\/custom/g' src/test/indexTest.ts 
sed -i 's/8000/8001/g' src/test/indexTest.ts
