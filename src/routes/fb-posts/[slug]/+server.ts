import { json, error } from '@sveltejs/kit';

export async function GET() {
  return json({
    cwd: process.cwd(),
    env_VERCEL: process.env.VERCEL,
    env_VERCEL_PROJECT_ROOT: process.env.VERCEL_PROJECT_ROOT_PATH,
    env_VERCEL_SYSTEM_HOME: process.env.VERCEL_SYSTEM_HOME,
    env_AWS_LAMBDA_FUNCTION_NAME: process.env.AWS_LAMBDA_FUNCTION_NAME,
    env_LD_LIBRARY_PATH: process.env.LD_LIBRARY_PATH,
    env_PATH: (process.env.PATH || '').split(':').slice(0, 5),
  });
}