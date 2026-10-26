import hashlib,hmac,importlib.util,pathlib,unittest
spec=importlib.util.spec_from_file_location('refresh',pathlib.Path(__file__).resolve().parents[1]/'scripts/refresh.py');refresh=importlib.util.module_from_spec(spec);spec.loader.exec_module(refresh)
class SigningTests(unittest.TestCase):
 def test_signature_binds_body_method_path_and_time(self):
  body=b'{"trigger":"schedule"}';secret='a'*64;stamp=1792980000
  headers=refresh.request_parts(secret,body,stamp)
  canonical='v1\n1792980000\nPOST\n/internal/import/\n'+hashlib.sha256(body).hexdigest()
  self.assertEqual(headers['X-AML-Timestamp'],str(stamp));self.assertEqual(headers['X-AML-Signature'],hmac.new(secret.encode(),canonical.encode(),hashlib.sha256).hexdigest())
  self.assertNotEqual(headers['X-AML-Signature'],refresh.request_parts(secret,b'{}',stamp)['X-AML-Signature'])
 def test_secret_is_not_a_request_header(self):
  headers=refresh.request_parts('b'*64,b'{}',1792980000)
  self.assertNotIn('b'*64,headers.values());self.assertNotIn('Authorization',headers)
if __name__=='__main__':unittest.main()
