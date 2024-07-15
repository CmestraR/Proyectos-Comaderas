from odoo.tests.common import TransactionCase


class TestBarcodeLabels(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestBarcodeLabels, cls).setUpClass()

        cls.product = cls.env["product.product"].create(
            {"name": "Product 1", "barcode": "982367918", "list_price": 100}
        )

        cls.config_rec = cls.env.ref(
            "customize_3label_barcode_layout.default_trbarcode_configuration"
        )

        user = cls.env["res.users"].create(
            {
                "name": "Leo Daniel",
                "login": "leo",
                "password": "leo123",
                "groups_id": [
                    (6, 0, cls.env.user.groups_id.ids),
                    (
                        4,
                        cls.env.ref(
                            "customize_3label_barcode_layout.group_3barcode_labels"
                        ).id,
                    ),
                ],
            }
        )
        user.partner_id.email = "leo@test.com"

        cls.env = cls.env(user=user)
        cls.cr = cls.env.cr

    def test_print_report(self):
        wizard = self.env["trbarcode.labels"].create(
            {
                "product_get_ids": [
                    (0, 0, {"wizard_id": 1, "product_id": self.product.id, "qty": 1.0})
                ]
            }
        )

        report = wizard.print_report()
        self.assertTrue(report, "El informe no se generó correctamente")

        paperformat = self.env.ref('customize_3label_barcode_layout.paperformat_trbarcode_label')
        self.assertTrue(paperformat, "El formato de papel no se creó correctamente")

        barcode_field = self.config_rec.barcode_field
        self.assertTrue(
            self.product[barcode_field],
            "No se configuró el código de barras para el producto",
        )

        report_data = report.get("data", {})
        product_ids = report_data.get("form", {}).get("product_ids", [])
        self.assertEqual(
            len(product_ids), 1, "El informe no contiene el producto esperado"
        )
        self.assertEqual(
            product_ids[0]["product_id"],
            self.product.id,
            "El informe no contiene el producto esperado",
        )
