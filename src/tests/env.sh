export FLASK_ENV=development
export APP_SETTINGS=src.config.DevelopmentConfig
export DATABASE_URL=postgresql://postgres:postgres@api-db:5432/api_dev
export DATABASE_TEST_URL=postgresql://postgres:postgres@api-db:5432/api_test
export DATABASE_LOCAL_URL=postgresql://postgres:postgres@localhost:5432/api_test
