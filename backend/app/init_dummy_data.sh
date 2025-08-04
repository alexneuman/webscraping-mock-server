#!/bin/bash
set -e

echo "🔍 Checking if dummy data is needed..."
# cd app
python -c "import asyncio; from app.utils import dummy_data; asyncio.run(dummy_data.generate_dummy_data())"