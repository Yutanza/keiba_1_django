# from django.db import models


# class Race(models.Model):
#     """
#     開催案内シートに対応するモデル。
#     レースに関する基本情報を保持します。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         blank=True,
#         null=True,
#         default=0
#     )
#     race_id = models.CharField(  # IntegerFieldからCharFieldに変更
#         max_length=20,
#         unique=True,
#         verbose_name='レースID'
#     )
#     race_name = models.CharField(
#         max_length=100,
#         verbose_name='レース名',
#         null=True,
#         blank=True
#     )
#     distance = models.IntegerField(
#         verbose_name='距離',
#         null=True,
#         blank=True
#     )  # 単位はメートル
#     weather = models.CharField(
#         max_length=50,
#         verbose_name='天候',
#         null=True,
#         blank=True
#     )
#     track_condition = models.CharField(
#         max_length=50,
#         verbose_name='馬場',
#         null=True,
#         blank=True
#     )
#     year = models.IntegerField(
#         verbose_name='開催年',
#         null=True,
#         blank=True
#     )
#     course = models.CharField(
#         max_length=100,
#         verbose_name='開催コース',
#         null=True,
#         blank=True
#     )
#     race_number = models.IntegerField(
#         verbose_name='開催回',
#         null=True,
#         blank=True
#     )
#     date = models.DateField(
#         verbose_name='開催日',
#         null=True,
#         blank=True
#     )
#     race_type = models.CharField(
#         max_length=50,
#         verbose_name='レースタイプ',
#         null=True,
#         blank=True
#     )
#     no = models.IntegerField(
#         verbose_name='No',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return f"{self.race_name} ({self.race_id})"


# class Horse(models.Model):
#     """
#     競走馬に関する情報を保持するモデル。
#     血統情報もここに含まれます。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         null=True,
#         blank=True
#     )
#     name = models.CharField(
#         max_length=100,
#         verbose_name='馬名'
#     )
#     sex_age = models.CharField(
#         max_length=10,
#         verbose_name='性齢',
#         null=True,
#         blank=True
#     )
#     birth_date = models.DateField(
#         verbose_name='生産年月',
#         null=True,
#         blank=True
#     )
#     trainer = models.ForeignKey(
#         'Trainer',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name='調教師'
#     )
#     breeder = models.ForeignKey(
#         'Breeder',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name='生産者'
#     )
#     sale_price = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='セリ取引価格'
#     )
#     sire = models.CharField(
#         max_length=100,
#         verbose_name='父',
#         null=True,
#         blank=True
#     )
#     dam = models.CharField(
#         max_length=100,
#         verbose_name='母',
#         null=True,
#         blank=True
#     )
#     damsire = models.CharField(
#         max_length=100,
#         verbose_name='母父',
#         null=True,
#         blank=True
#     )
    

#     def __str__(self):
#         return self.name


# class Jockey(models.Model):
#     """
#     騎手に関する情報を保持するモデル。
#     """
#     name = models.CharField(
#         max_length=100,
#         unique=False,
#         verbose_name='騎手名'
#     )

#     def __str__(self):
#         return self.name


# class Trainer(models.Model):
#     """
#     調教師に関する情報を保持するモデル。
#     """
#     name = models.CharField(
#         max_length=100,
#         unique=False,
#         verbose_name='調教師名'
#     )

#     def __str__(self):
#         return self.name


# class Breeder(models.Model):
#     """
#     生産者に関する情報を保持するモデル。
#     """
#     name = models.CharField(
#         max_length=100,
#         unique=True,
#         verbose_name='生産者名'
#     )

#     def __str__(self):
#         return self.name


# class RaceEntry(models.Model):
#     """
#     出馬表シートに対応するモデル。
#     レースへのエントリー情報を保持します。
#     """
#     order_of_finish = models.IntegerField(  # フィールド名をPEP8準拠に変更
#         verbose_name='順位',
#         null=True,
#         blank=True
#     )
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE,
#         related_name='entries',
#         verbose_name='レース'
#     )
#     gate = models.IntegerField(
#         verbose_name='枠',
#         null=True,
#         blank=True
#     )
#     horse_number = models.IntegerField(
#         verbose_name='馬番',
#         null=True,
#         blank=True
#     )
#     horse = models.ForeignKey(
#         Horse,
#         on_delete=models.CASCADE,
#         related_name='entries',
#         verbose_name='馬'
#     )
#     weight_carried = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         verbose_name='斤量',
#         null=True,
#         blank=True
#     )
#     jockey = models.ForeignKey(
#         Jockey,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name='騎手'
#     )
#     trainer = models.ForeignKey(
#         Trainer,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name='厩舎'
#     )
#     body_weight_change = models.DecimalField(
#         max_digits=5,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='馬体重(増減)'
#     )
#     odds = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='オッズ（更新）'
#     )
#     popularity = models.IntegerField(
#         null=True,
#         blank=True,
#         verbose_name='人気'
#     )

#     def __str__(self):
#         return f"{self.race} - {self.horse.name} (枠{self.gate} 番{self.horse_number})"


# class Payout(models.Model):
#     """
#     払戻シートに対応するモデル。
#     レースの払戻情報を保持します。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         null=True,
#         blank=True
#     )
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE,
#         related_name='payouts',
#         verbose_name='レース'
#     )
#     category = models.CharField(
#         max_length=50,
#         verbose_name='項目',
#         null=True,
#         blank=True
#     )  # 例: 単勝, 複勝, 馬連 など
#     horse_gate = models.IntegerField(
#         verbose_name='馬枠',
#         null=True,
#         blank=True
#     )
#     amount = models.DecimalField(
#         max_digits=30,
#         decimal_places=1,
#         verbose_name='金額',
#         null=True,
#         blank=True
#     )  # 円
#     popularity = models.IntegerField(
#         null=True,
#         blank=True,
#         verbose_name='人気'
#     )

#     def __str__(self):
#         return f"{self.race} - {self.category} - 枠{self.horse_gate}"


# class CornerPassageRank(models.Model):
#     """
#     コーナー通過順位シートに対応するモデル。
#     各コーナーでの通過順位を保持します。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         null=True,
#         blank=True
#     )
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE,
#         related_name='corner_passages',
#         verbose_name='レース'
#     )
#     corner = models.CharField(
#         max_length=50,
#         verbose_name='コーナー',
#         null=True,
#         blank=True
#     )  # 例: 第1コーナー, 第2コーナー など
#     passage_order = models.IntegerField(
#         verbose_name='通過順位',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return f"{self.race} - {self.corner} - 順位 {self.passage_order}"


# class LapTime(models.Model):
#     """
#     ラップタイムシートに対応するモデル。
#     各区間のタイムを保持します。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         null=True,
#         blank=True
#     )
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE,
#         related_name='lap_times',
#         verbose_name='レース'
#     )
#     category = models.CharField(
#         max_length=50,
#         verbose_name='項目',
#         null=True,
#         blank=True
#     )  # 例: 上り, 中山 など
#     m200 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='200m'
#     )
#     m400 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='400m'
#     )
#     m600 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='600m'
#     )
#     m800 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='800m'
#     )
#     m1000 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='1000m'
#     )
#     m1200 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='1200m'
#     )
#     m1400 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='1400m'
#     )
#     m1600 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='1600m'
#     )
#     m1800 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='1800m'
#     )
#     m2000 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='2000m'
#     )
#     m2200 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='2200m'
#     )
#     m2400 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='2400m'
#     )
#     m2600 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='2600m'
#     )
#     m2800 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='2800m'
#     )
#     m3000 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='3000m'
#     )
#     m3200 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='3200m'
#     )
#     m3400 = models.DecimalField(
#         max_digits=6,
#         decimal_places=2,
#         null=True,
#         blank=True,
#         verbose_name='3400m'
#     )

#     def __str__(self):
#         return f"{self.race} - {self.category}"


# class Pedigree(models.Model):
#     """
#     血統シートに対応するモデル。
#     競走馬の血統情報を保持します。
#     """
#     item = models.IntegerField(
#         verbose_name='項',
#         null=True,
#         blank=True
#     )
#     horse = models.OneToOneField(
#         Horse,
#         on_delete=models.CASCADE,
#         related_name='pedigree',
#         verbose_name='競走馬'
#     )
#     sire = models.CharField(
#         max_length=100,
#         verbose_name='父',
#         null=True,
#         blank=True
#     )
#     dam = models.CharField(
#         max_length=100,
#         verbose_name='母',
#         null=True,
#         blank=True
#     )
#     damsire = models.CharField(
#         max_length=100,
#         verbose_name='母父',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return f"Pedigree of {self.horse.name}"


# class RaceHTML(models.Model):
#     """
#     レースのHTMLデータを保持するモデル。
#     """
#     race_id = models.IntegerField(
#         unique=True,
#         verbose_name='レースID',
#         null=False
#     )
#     html_text = models.TextField(
#         verbose_name='HTMLテキスト',
#         null=True,
#         blank=True
#     )

#     def __str__(self):
#         return str(self.race_id)

###再定義版

from django.db import models

class Race(models.Model):
    """
    開催案内シートに対応するモデル。
    レースに関する基本情報を保持します。
    """
    item = models.IntegerField(
        verbose_name='項',
        blank=True,
        null=True,
        default=0
    )
    race_id = models.CharField(  # IntegerFieldからCharFieldに変更
        max_length=20,
        unique=True,
        verbose_name='レースID'
    )
    race_name = models.CharField(
        max_length=100,
        verbose_name='レース名',
        null=True,
        blank=True
    )
    distance = models.IntegerField(
        verbose_name='距離',
        null=True,
        blank=True
    )  # 単位はメートル
    weather = models.CharField(
        max_length=50,
        verbose_name='天候',
        null=True,
        blank=True
    )
    track_condition = models.CharField(
        max_length=50,
        verbose_name='馬場',
        null=True,
        blank=True
    )
    year = models.IntegerField(
        verbose_name='開催年',
        null=True,
        blank=True
    )
    course = models.CharField(
        max_length=100,
        verbose_name='開催コース',
        null=True,
        blank=True
    )
    race_number = models.IntegerField(
        verbose_name='開催回',
        null=True,
        blank=True
    )
    date = models.DateField(
        verbose_name='開催日',
        null=True,
        blank=True
    )
    race_type = models.CharField(
        max_length=50,
        verbose_name='レースタイプ',
        null=True,
        blank=True
    )
    no = models.IntegerField(
        verbose_name='No',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.race_name} ({self.race_id})"


class Horse(models.Model):
    """
    競走馬に関する情報を保持するモデル。
    血統情報もここに含まれます。
    """
    item = models.IntegerField(
        verbose_name='項',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='馬名'
    )
    sex_age = models.CharField(
        max_length=10,
        verbose_name='性齢',
        null=True,
        blank=True
    )
    birth_date = models.DateField(
        verbose_name='生産年月',
        null=True,
        blank=True
    )
    trainer = models.ForeignKey(
        'Trainer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='調教師'
    )
    breeder = models.ForeignKey(
        'Breeder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='生産者'
    )
    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='セリ取引価格'
    )
    sire = models.CharField(
        max_length=100,
        verbose_name='父',
        null=True,
        blank=True
    )
    dam = models.CharField(
        max_length=100,
        verbose_name='母',
        null=True,
        blank=True
    )
    damsire = models.CharField(
        max_length=100,
        verbose_name='母父',
        null=True,
        blank=True
    )
    horse_netkeiba_id = models.IntegerField(  # ★追加
        verbose_name='馬netkeibaID',
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Jockey(models.Model):
    """
    騎手に関する情報を保持するモデル。
    """
    name = models.CharField(
        max_length=100,
        unique=False,
        verbose_name='騎手名'
    )
    jockey_netkeiba_id = models.IntegerField(  # ★追加
        verbose_name='騎手netkeibaID',
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Trainer(models.Model):
    """
    調教師に関する情報を保持するモデル。
    """
    name = models.CharField(
        max_length=100,
        unique=False,
        verbose_name='調教師名'
    )
    trainer_netkeiba_id = models.IntegerField(  # ★追加
        verbose_name='調教師netkeibaID',
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Breeder(models.Model):
    """
    生産者に関する情報を保持するモデル。
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='生産者名'
    )

    def __str__(self):
        return self.name


class Owner(models.Model):
    """
    馬主に関する情報を保持するモデル。
    """
    name = models.CharField(
        max_length=100,
        verbose_name='馬主名'
    )
    owner_netkeiba_id = models.IntegerField(  # ★追加
        verbose_name='馬主netkeibaID',
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class RaceEntry(models.Model):
    """
    出馬表シートに対応するモデル。
    レースへのエントリー情報を保持します。
    """
    order_of_finish = models.IntegerField(  # フィールド名をPEP8準拠に変更
        verbose_name='順位',
        null=True,
        blank=True
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='レース'
    )
    gate = models.IntegerField(
        verbose_name='枠',
        null=True,
        blank=True
    )
    horse_number = models.IntegerField(
        verbose_name='馬番',
        null=True,
        blank=True
    )
    horse = models.ForeignKey(
        Horse,
        on_delete=models.CASCADE,
        related_name='entries',
        verbose_name='馬'
    )
    weight_carried = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='斤量',
        null=True,
        blank=True
    )
    jockey = models.ForeignKey(
        Jockey,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='騎手'
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='厩舎'
    )
    owner = models.ForeignKey(  # ★追加
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='馬主'
    )
    body_weight_change = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='馬体重(増減)'
    )
    odds = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='オッズ（更新）'
    )
    popularity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='人気'
    )
    # 追加フィールド（必要に応じて）
    # horse_netkeiba_id = models.IntegerField( # オプション
    #     verbose_name='馬netkeibaID',
    #     null=True,
    #     blank=True
    # )
    # jockey_netkeiba_id = models.IntegerField( # オプション
    #     verbose_name='騎手netkeibaID',
    #     null=True,
    #     blank=True
    # )
    # trainer_netkeiba_id = models.IntegerField( # オプション
    #     verbose_name='調教師netkeibaID',
    #     null=True,
    #     blank=True
    # )
    # owner_netkeiba_id = models.IntegerField( # オプション
    #     verbose_name='馬主netkeibaID',
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return f"{self.race} - {self.horse.name} (枠{self.gate} 番{self.horse_number})"


class Payout(models.Model):
    """
    払戻シートに対応するモデル。
    レースの払戻情報を保持します。
    """
    item = models.IntegerField(
        verbose_name='項',
        null=True,
        blank=True
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='payouts',
        verbose_name='レース'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='項目',
        null=True,
        blank=True
    )  # 例: 単勝, 複勝, 馬連 など
    horse_gate = models.IntegerField(
        verbose_name='馬枠',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=1,
        verbose_name='金額',
        null=True,
        blank=True
    )  # 円
    popularity = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='人気'
    )

    def __str__(self):
        return f"{self.race} - {self.category} - 枠{self.horse_gate}"


class CornerPassageRank(models.Model):
    """
    コーナー通過順位シートに対応するモデル。
    各コーナーでの通過順位を保持します。
    """
    item = models.IntegerField(
        verbose_name='項',
        null=True,
        blank=True
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='corner_passages',
        verbose_name='レース'
    )
    corner = models.CharField(
        max_length=50,
        verbose_name='コーナー',
        null=True,
        blank=True
    )  # 例: 第1コーナー, 第2コーナー など
    passage_order = models.IntegerField(
        verbose_name='通過順位',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.race} - {self.corner} - 順位 {self.passage_order}"


class LapTime(models.Model):
    """
    ラップタイムシートに対応するモデル。
    各区間のタイムを保持します。
    """
    item = models.IntegerField(
        verbose_name='項',
        null=True,
        blank=True
    )
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name='lap_times',
        verbose_name='レース'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='項目',
        null=True,
        blank=True
    )  # 例: 上り, 中山 など
    m200 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='200m'
    )
    m400 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='400m'
    )
    m600 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='600m'
    )
    m800 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='800m'
    )
    m1000 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='1000m'
    )
    m1200 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='1200m'
    )
    m1400 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='1400m'
    )
    m1600 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='1600m'
    )
    m1800 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='1800m'
    )
    m2000 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='2000m'
    )
    m2200 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='2200m'
    )
    m2400 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='2400m'
    )
    m2600 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='2600m'
    )
    m2800 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='2800m'
    )
    m3000 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='3000m'
    )
    m3200 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='3200m'
    )
    m3400 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='3400m'
    )

    def __str__(self):
        return f"{self.race} - {self.category}"


class Pedigree(models.Model):
    """
    血統シートに対応するモデル。
    競走馬の血統情報を保持します。
    """
    item = models.IntegerField(
        verbose_name='項',
        null=True,
        blank=True
    )
    horse = models.OneToOneField(
        Horse,
        on_delete=models.CASCADE,
        related_name='pedigree',
        verbose_name='競走馬'
    )
    sire = models.CharField(
        max_length=100,
        verbose_name='父',
        null=True,
        blank=True
    )
    dam = models.CharField(
        max_length=100,
        verbose_name='母',
        null=True,
        blank=True
    )
    damsire = models.CharField(
        max_length=100,
        verbose_name='母父',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Pedigree of {self.horse.name}"


class RaceHTML(models.Model):
    """
    レースのHTMLデータを保持するモデル。
    """
    race_id = models.IntegerField(
        unique=True,
        verbose_name='レースID',
        null=False
    )
    html_text = models.TextField(
        verbose_name='HTMLテキスト',
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.race_id)


