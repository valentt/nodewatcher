#!/usr/bin/env python
"""
Convenience script to run E2E tests with common configurations.
"""
import os
import sys
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='Run Nodewatcher E2E tests')
    parser.add_argument('--url', default='http://localhost:8000',
                        help='Nodewatcher base URL')
    parser.add_argument('--user', default='admin',
                        help='Admin username')
    parser.add_argument('--password', default='admin',
                        help='Admin password')
    parser.add_argument('--browser', choices=['chrome', 'firefox'],
                        default='chrome', help='Browser to use')
    parser.add_argument('--visible', action='store_true',
                        help='Run with visible browser (non-headless)')
    parser.add_argument('--html', action='store_true',
                        help='Generate HTML report')
    parser.add_argument('--parallel', type=int, default=0,
                        help='Run tests in parallel (number of workers)')
    parser.add_argument('tests', nargs='*', default=[],
                        help='Specific tests to run')

    args = parser.parse_args()

    # Set environment variables
    env = os.environ.copy()
    env['NODEWATCHER_URL'] = args.url
    env['NODEWATCHER_ADMIN_USER'] = args.user
    env['NODEWATCHER_ADMIN_PASS'] = args.password
    env['SELENIUM_BROWSER'] = args.browser
    env['SELENIUM_HEADLESS'] = 'false' if args.visible else 'true'

    # Build pytest command
    cmd = ['pytest', '-v']

    if args.html:
        cmd.extend(['--html=report.html', '--self-contained-html'])

    if args.parallel > 0:
        cmd.extend(['-n', str(args.parallel)])

    if args.tests:
        cmd.extend(args.tests)

    # Run tests
    print(f'Running: {" ".join(cmd)}')
    print(f'URL: {args.url}')
    print(f'Browser: {args.browser}')
    print(f'Headless: {not args.visible}')
    print()

    result = subprocess.run(cmd, env=env, cwd=os.path.dirname(__file__))
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
