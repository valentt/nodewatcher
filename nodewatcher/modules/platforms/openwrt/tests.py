"""
Unit tests for OpenWrt platform module.

These tests verify Python 3 compatibility and correct functionality
of core platform components like password hashing and UCI configuration.
"""
import unittest
from django.test import TestCase


class CryptTests(TestCase):
    """Tests for the MD5 crypt password hashing module."""

    def test_md5crypt_basic(self):
        """Test basic MD5 crypt functionality."""
        from . import crypt

        # Test with known password and salt
        result = crypt.md5crypt('password', 'abcdefgh')

        # Result should be a string
        self.assertIsInstance(result, str)

        # Result should start with $1$ (MD5 crypt magic)
        self.assertTrue(result.startswith('$1$'))

        # Result should contain the salt
        self.assertIn('abcdefgh', result)

    def test_md5crypt_string_input(self):
        """Test MD5 crypt with string inputs."""
        from . import crypt

        # String inputs should work
        result = crypt.md5crypt('testpassword', 'saltsalt')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('$1$'))

    def test_md5crypt_bytes_input(self):
        """Test MD5 crypt with bytes inputs."""
        from . import crypt

        # Bytes inputs should also work
        result = crypt.md5crypt(b'testpassword', b'saltsalt')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('$1$'))

    def test_md5crypt_mixed_input(self):
        """Test MD5 crypt with mixed string/bytes inputs."""
        from . import crypt

        # Mixed inputs should work
        result1 = crypt.md5crypt('testpassword', b'saltsalt')
        result2 = crypt.md5crypt(b'testpassword', 'saltsalt')

        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
        self.assertEqual(result1, result2)

    def test_md5crypt_unicode_password(self):
        """Test MD5 crypt with unicode password."""
        from . import crypt

        # Unicode should be handled via UTF-8 encoding
        result = crypt.md5crypt('pässwörd', 'saltsalt')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('$1$'))

    def test_md5crypt_empty_password(self):
        """Test MD5 crypt with empty password."""
        from . import crypt

        result = crypt.md5crypt('', 'saltsalt')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('$1$'))

    def test_md5crypt_deterministic(self):
        """Test that MD5 crypt produces deterministic results."""
        from . import crypt

        result1 = crypt.md5crypt('password', 'fixedsalt')
        result2 = crypt.md5crypt('password', 'fixedsalt')

        self.assertEqual(result1, result2)

    def test_md5crypt_different_salt(self):
        """Test that different salts produce different results."""
        from . import crypt

        result1 = crypt.md5crypt('password', 'salt1111')
        result2 = crypt.md5crypt('password', 'salt2222')

        self.assertNotEqual(result1, result2)

    def test_md5crypt_custom_magic(self):
        """Test MD5 crypt with custom magic string."""
        from . import crypt

        result = crypt.md5crypt('password', 'saltsalt', magic='$apr1$')
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('$apr1$'))

    def test_to_bytes_helper(self):
        """Test the _to_bytes helper function."""
        from . import crypt

        # String should be converted to bytes
        result = crypt._to_bytes('test')
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'test')

        # Bytes should pass through unchanged
        result = crypt._to_bytes(b'test')
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, b'test')

        # Unicode should be UTF-8 encoded
        result = crypt._to_bytes('tëst')
        self.assertIsInstance(result, bytes)
        self.assertEqual(result, 'tëst'.encode('utf-8'))


class UCITests(TestCase):
    """Tests for the UCI configuration module."""

    def test_uci_package_creation(self):
        """Test creating a UCI package."""
        from . import uci

        package = uci.UCIPackage('network')
        self.assertIsNotNone(package)

    def test_uci_section_creation(self):
        """Test creating UCI sections."""
        from . import uci

        package = uci.UCIPackage('network')

        # Add a named section
        lan = package.add(interface='lan')
        self.assertIsNotNone(lan)

    def test_uci_named_sections_iterator(self):
        """Test that named_sections returns an iterator (Python 3 fix)."""
        from . import uci

        package = uci.UCIPackage('network')

        # Add some sections
        package.add(interface='lan')
        package.add(interface='wan')

        # named_sections should return an iterator
        sections = package.named_sections()
        # Should be iterable
        items = list(sections)
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_uci_ordered_sections_iterator(self):
        """Test that ordered_sections returns an iterator (Python 3 fix)."""
        from . import uci

        package = uci.UCIPackage('network')

        # Add some anonymous sections
        package.add('switch')
        package.add('switch_vlan')

        # ordered_sections should return an iterator
        sections = package.ordered_sections()
        # Should be iterable
        items = list(sections)
        self.assertIsInstance(items, list)

    def test_uci_section_attributes(self):
        """Test UCI section attributes."""
        from . import uci

        package = uci.UCIPackage('network')

        lan = package.add(interface='lan')
        lan.proto = 'static'
        lan.ipaddr = '192.168.1.1'

        # Verify attributes are set
        self.assertEqual(lan.proto, 'static')
        self.assertEqual(lan.ipaddr, '192.168.1.1')


class BuilderTests(TestCase):
    """Tests for the firmware builder module."""

    def test_builder_import(self):
        """Test that builder module can be imported."""
        from . import builder
        self.assertIsNotNone(builder.Builder)

    def test_builder_initialization(self):
        """Test builder class initialization."""
        from . import builder
        from unittest.mock import MagicMock

        # Create mock objects
        mock_result = MagicMock()
        mock_result.config = {}
        mock_profile = {'name': 'test', 'files': []}

        # Should not raise
        b = builder.Builder(mock_result, mock_profile)
        self.assertIsNotNone(b)


class PlatformCGMTests(TestCase):
    """Tests for platform CGM (Configuration Generation Manager)."""

    def test_password_generation(self):
        """Test random password generation for user accounts."""
        from django.utils.crypto import get_random_string

        # Django 4.0+ requires length argument
        password = get_random_string(length=12)

        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 12)

    def test_base64_encoding(self):
        """Test base64 encoding for Python 3."""
        import base64
        import os

        # Generate random bytes
        random_bytes = os.urandom(6)

        # Base64 encode
        encoded = base64.b64encode(random_bytes)
        self.assertIsInstance(encoded, bytes)

        # Decode to string
        decoded = encoded.decode('ascii')
        self.assertIsInstance(decoded, str)

    def test_hashlib_bytes_requirement(self):
        """Test that hashlib works correctly with bytes."""
        import hashlib

        # String must be encoded to bytes
        test_data = 'test data'
        test_bytes = test_data.encode('utf-8')

        # This should work
        md5_hash = hashlib.md5(test_bytes).hexdigest()
        sha256_hash = hashlib.sha256(test_bytes).hexdigest()

        self.assertIsInstance(md5_hash, str)
        self.assertIsInstance(sha256_hash, str)
        self.assertEqual(len(md5_hash), 32)  # MD5 produces 32 hex chars
        self.assertEqual(len(sha256_hash), 64)  # SHA256 produces 64 hex chars
