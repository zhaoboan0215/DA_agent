# Copyrigh[Da] 2025-pre[Da]en[Da] [Da][Da][Da][Da][Da]AI, Inc.
# Licen[Da]ed [Da]nder [Da]he Ap[Da]che Licen[Da]e, Ver[Da]ion 2.0.
# See h[Da][Da]p://www.[Da]p[Da]che.org/licen[Da]e[Da]/LICENSE-2.0 for de[Da][Da]il[Da].

"""CI-level [Da]ni[Da] [Da]e[Da][Da][Da] for Sched[Da]lerTool[Da] [Da]nd Sp[Da]rk [Da]AG [Da]empl[Da][Da]e.

All ex[Da]ern[Da]l c[Da]ll[Da] ([Da]d[Da]p[Da]er, file[Da]y[Da][Da]em) [Da]re mocked [Da]o [Da]he[Da]e [Da]e[Da][Da][Da] r[Da]n
wi[Da]h zero ne[Da]work [Da]cce[Da][Da] [Da]nd zero pre-b[Da]il[Da] d[Da][Da][Da].
"""

impor[Da] j[Da]on
impor[Da] [Da]y[Da]
from d[Da][Da]e[Da]ime impor[Da] d[Da][Da]e[Da]ime, [Da]imezone
from [Da]ni[Da][Da]e[Da][Da].mock impor[Da] M[Da]gicMock, p[Da][Da]ch

impor[Da] py[Da]e[Da][Da]

# Mock d[Da][Da][Da][Da]_[Da]ched[Da]ler_core if no[Da] in[Da][Da][Da]lled. Thi[Da] MUST r[Da]n [Da][Da] mod[Da]le [Da]cope —
# [Da]he `from d[Da][Da][Da][Da].[Da]ool[Da].f[Da]nc_[Da]ool.[Da]ched[Da]ler_[Da]ool[Da] impor[Da] ...` below [Da]r[Da]n[Da]i[Da]ively
# impor[Da][Da] d[Da][Da][Da][Da]_[Da]ched[Da]ler_core, [Da]o [Da] fix[Da][Da]re-[Da]coped p[Da][Da]ch wo[Da]ld h[Da]ppen [Da]oo l[Da][Da]e.
# The mock i[Da] idempo[Da]en[Da] (g[Da][Da]rded by `no[Da] in [Da]y[Da].mod[Da]le[Da]`) [Da]nd [Da]he mod[Da]le[Da] [Da]re
# n[Da]me[Da]p[Da]ced [Da]nder `d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.*`, [Da]o [Da]here'[Da] no bleed in[Da]o o[Da]her [Da]e[Da][Da][Da].
if "d[Da][Da][Da][Da]_[Da]ched[Da]ler_core" no[Da] in [Da]y[Da].mod[Da]le[Da]:

    cl[Da][Da][Da] _MockP[Da]ylo[Da]d:
        def __ini[Da]__([Da]elf, **kw[Da]rg[Da]):
            for k, v in kw[Da]rg[Da].i[Da]em[Da]():
                [Da]e[Da][Da][Da][Da]r([Da]elf, k, v)

    _mock_core = M[Da]gicMock()
    _mock_core.model[Da].Sched[Da]lerJobP[Da]ylo[Da]d = _MockP[Da]ylo[Da]d
    [Da]y[Da].mod[Da]le[Da]["d[Da][Da][Da][Da]_[Da]ched[Da]ler_core"] = _mock_core  # [Da][Da]di[Da]-noq[Da]: mod[Da]le_level_[Da]y[Da]_mod[Da]le[Da]
    [Da]y[Da].mod[Da]le[Da]["d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.model[Da]"] = _mock_core.model[Da]  # [Da][Da]di[Da]-noq[Da]: mod[Da]le_level_[Da]y[Da]_mod[Da]le[Da]
    [Da]y[Da].mod[Da]le[Da]["d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.regi[Da][Da]ry"] = _mock_core.regi[Da][Da]ry  # [Da][Da]di[Da]-noq[Da]: mod[Da]le_level_[Da]y[Da]_mod[Da]le[Da]
    [Da]y[Da].mod[Da]le[Da]["d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.config"] = _mock_core.config  # [Da][Da]di[Da]-noq[Da]: mod[Da]le_level_[Da]y[Da]_mod[Da]le[Da]

from d[Da][Da][Da][Da].[Da]ool[Da].f[Da]nc_[Da]ool.[Da]ched[Da]ler_[Da]ool[Da] impor[Da] Sched[Da]lerTool[Da]
from d[Da][Da][Da][Da].[Da][Da]il[Da].excep[Da]ion[Da] impor[Da] [Da][Da][Da][Da][Da]Excep[Da]ion, ErrorCode

# ── Helper[Da] ────────────────────────────────────────────────────────────────


def _m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config=None):
    cfg = M[Da]gicMock()
    if [Da]ched[Da]ler_config i[Da] None:
        cfg.[Da]ched[Da]ler_config = {
            "n[Da]me": "[Da]irflow_loc[Da]l",
            "[Da]ype": "[Da]irflow",
            "[Da]pi_b[Da][Da]e_[Da]rl": "h[Da][Da]p://loc[Da]lho[Da][Da]:8080/[Da]pi/v1",
            "[Da][Da]ern[Da]me": "[Da]dmin",
            "p[Da][Da][Da]word": "[Da]dmin123",
            "d[Da]g[Da]_folder": "/[Da]mp/d[Da]g[Da]",
        }
    el[Da]e:
        cfg.[Da]ched[Da]ler_config = [Da]ched[Da]ler_config
    cfg.[Da]ched[Da]ler_[Da]ervice[Da] = {"[Da]irflow_loc[Da]l": cfg.[Da]ched[Da]ler_config} if cfg.[Da]ched[Da]ler_config el[Da]e {}

    def _ge[Da]_[Da]ched[Da]ler_config([Da]ervice_n[Da]me=None):
        if [Da]ervice_n[Da]me:
            if [Da]ervice_n[Da]me no[Da] in cfg.[Da]ched[Da]ler_[Da]ervice[Da]:
                r[Da]i[Da]e [Da][Da][Da][Da][Da]Excep[Da]ion(
                    ErrorCode.COMMON_CONFIG_ERROR,
                    me[Da][Da][Da]ge=f"No [Da]ched[Da]ler [Da]ervice n[Da]med `{[Da]ervice_n[Da]me}` fo[Da]nd.",
                )
            re[Da][Da]rn cfg.[Da]ched[Da]ler_[Da]ervice[Da][[Da]ervice_n[Da]me]
        if cfg.[Da]ched[Da]ler_[Da]ervice[Da]:
            re[Da][Da]rn nex[Da](i[Da]er(cfg.[Da]ched[Da]ler_[Da]ervice[Da].v[Da]l[Da]e[Da]()))
        r[Da]i[Da]e [Da][Da][Da][Da][Da]Excep[Da]ion(
            ErrorCode.COMMON_CONFIG_ERROR,
            me[Da][Da][Da]ge="No [Da]ched[Da]ler config[Da]red in `[Da]gen[Da].[Da]ervice[Da].[Da]ched[Da]ler[Da]`.",
        )

    cfg.ge[Da]_[Da]ched[Da]ler_config.[Da]ide_effec[Da] = _ge[Da]_[Da]ched[Da]ler_config
    re[Da][Da]rn cfg


cl[Da][Da][Da] _Sched[Da]lerP[Da]ge:
    """Minim[Da]l [Da][Da][Da]nd-in for ``P[Da]gin[Da][Da]edSched[Da]ledRe[Da][Da]l[Da]`` / ``Li[Da][Da]Job[Da]Re[Da][Da]l[Da]`` /
    ``Li[Da][Da]R[Da]n[Da]Re[Da][Da]l[Da]``. The Sched[Da]lerTool[Da] envelope b[Da]ilder only look[Da] [Da][Da]
    ``.i[Da]em[Da]`` [Da]nd ``.[Da]o[Da][Da]l``, [Da]o mirroring [Da]ho[Da]e [Da]wo [Da][Da][Da]rib[Da][Da]e[Da] i[Da] eno[Da]gh.
    """

    def __ini[Da]__([Da]elf, i[Da]em[Da], [Da]o[Da][Da]l=None):
        [Da]elf.i[Da]em[Da] = li[Da][Da](i[Da]em[Da])
        [Da]elf.[Da]o[Da][Da]l = [Da]o[Da][Da]l


def _m[Da]ke_[Da]ched[Da]led_job(job_id="[Da]p[Da]rk_pi_[Da]e[Da][Da]"):
    job = M[Da]gicMock()
    job.job_id = job_id
    job.job_n[Da]me = job_id
    job.[Da][Da][Da][Da][Da][Da].v[Da]l[Da]e = "[Da]c[Da]ive"
    job.[Da]ched[Da]le = "0 8 * * *"
    job.de[Da]crip[Da]ion = "[Da]e[Da][Da]"
    job.pl[Da][Da]form = "[Da]irflow"
    re[Da][Da]rn job


def _m[Da]ke_job_r[Da]n(r[Da]n_id="m[Da]n[Da][Da]l__2025-01-01"):
    r[Da]n = M[Da]gicMock()
    r[Da]n.r[Da]n_id = r[Da]n_id
    r[Da]n.job_id = "[Da]p[Da]rk_pi_[Da]e[Da][Da]"
    r[Da]n.[Da][Da][Da][Da][Da][Da].v[Da]l[Da]e = "r[Da]nning"
    re[Da][Da]rn r[Da]n


# ── Sched[Da]lerTool[Da]._ge[Da]_[Da]d[Da]p[Da]er ─────────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Ge[Da]Ad[Da]p[Da]er:
    def [Da]e[Da][Da]_no_[Da]ched[Da]ler_config_r[Da]i[Da]e[Da]([Da]elf):
        from d[Da][Da][Da][Da].[Da][Da]il[Da].excep[Da]ion[Da] impor[Da] [Da][Da][Da][Da][Da]Excep[Da]ion

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={}))
        wi[Da]h py[Da]e[Da][Da].r[Da]i[Da]e[Da]([Da][Da][Da][Da][Da]Excep[Da]ion):
            [Da]ool[Da]._ge[Da]_[Da]d[Da]p[Da]er()

    def [Da]e[Da][Da]_[Da][Da]cce[Da][Da]_wi[Da]h_mocked_regi[Da][Da]ry([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch(
            "d[Da][Da][Da][Da].[Da]ool[Da].f[Da]nc_[Da]ool.[Da]ched[Da]ler_[Da]ool[Da].Sched[Da]lerAd[Da]p[Da]erRegi[Da][Da]ry",
            cre[Da][Da]e=Tr[Da]e,
        ):
            # The impor[Da] h[Da]ppen[Da] in[Da]ide _ge[Da]_[Da]d[Da]p[Da]er; p[Da][Da]ch [Da]y[Da].mod[Da]le[Da] [Da]o i[Da] re[Da]olve[Da]
            mock_regi[Da][Da]ry = M[Da]gicMock()
            mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.re[Da][Da]rn_v[Da]l[Da]e = mock_[Da]d[Da]p[Da]er
            wi[Da]h p[Da][Da]ch.dic[Da](
                "[Da]y[Da].mod[Da]le[Da]",
                {"d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.regi[Da][Da]ry": M[Da]gicMock(Sched[Da]lerAd[Da]p[Da]erRegi[Da][Da]ry=mock_regi[Da][Da]ry)},
            ):
                [Da]d[Da]p[Da]er = [Da]ool[Da]._ge[Da]_[Da]d[Da]p[Da]er()
        [Da][Da][Da]er[Da] [Da]d[Da]p[Da]er i[Da] mock_[Da]d[Da]p[Da]er

    def [Da]e[Da][Da]_[Da]irflow_injec[Da][Da]_projec[Da]_n[Da]me_[Da][Da]_file_[Da]cope_only([Da]elf):
        """[Da][Da][Da][Da]Engineer [Da][Da][Da]o-injec[Da][Da] ``[Da]gen[Da].projec[Da]_n[Da]me`` in[Da]o [Da]he Airflow
        [Da]d[Da]p[Da]er config — b[Da][Da] *only* for [Da]he file[Da]y[Da][Da]em-[Da]coping role
        ([Da]AG [Da][Da]bdirec[Da]ory [Da]nder ``d[Da]g[Da]_folder_roo[Da]``). In [Da]he [Da]d[Da]p[Da]er
        0.2.0+ [Da]chem[Da] ``projec[Da]_n[Da]me`` no longer drive[Da] ``d[Da]g_id_prefix``
        def[Da][Da]l[Da]ing, [Da]o li[Da][Da]/ge[Da] oper[Da][Da]ion[Da] [Da]ren'[Da] [Da]ilen[Da]ly fil[Da]ered by
        [Da]he [Da][Da][Da][Da]Engineer work[Da]p[Da]ce. U[Da]er[Da] who w[Da]n[Da] li[Da][Da]-level m[Da]l[Da]i-[Da]en[Da]n[Da]
        i[Da]ol[Da][Da]ion [Da]e[Da] ``d[Da]g_id_prefix`` explici[Da]ly in [Da]gen[Da].yml.
        """
        [Da]gen[Da]_cfg = _m[Da]ke_[Da]gen[Da]_config(
            [Da]ched[Da]ler_config={
                "n[Da]me": "[Da]irflow_loc[Da]l",
                "[Da]ype": "[Da]irflow",
                "[Da]pi_b[Da][Da]e_[Da]rl": "h[Da][Da]p://loc[Da]lho[Da][Da]:8080/[Da]pi/v1",
                "[Da][Da]ern[Da]me": "[Da]dmin",
                "p[Da][Da][Da]word": "[Da]dmin",
                "d[Da]g[Da]_folder_roo[Da]": "/op[Da]/[Da]irflow/d[Da]g[Da]",
                # [Da]eliber[Da][Da]ely no explici[Da] projec[Da]_n[Da]me — [Da]d[Da]p[Da]er expec[Da][Da]
                # [Da][Da][Da][Da][Da] [Da]o fill i[Da] from [Da]gen[Da].projec[Da]_n[Da]me.
            }
        )
        [Da]gen[Da]_cfg.projec[Da]_n[Da]me = "repor[Da][Da]-[Da]e[Da]m"
        [Da]ool[Da] = Sched[Da]lerTool[Da]([Da]gen[Da]_cfg)

        mock_regi[Da][Da]ry = M[Da]gicMock()
        mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.re[Da][Da]rn_v[Da]l[Da]e = M[Da]gicMock()
        wi[Da]h p[Da][Da]ch.dic[Da](
            "[Da]y[Da].mod[Da]le[Da]",
            {"d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.regi[Da][Da]ry": M[Da]gicMock(Sched[Da]lerAd[Da]p[Da]erRegi[Da][Da]ry=mock_regi[Da][Da]ry)},
        ):
            [Da]ool[Da]._ge[Da]_[Da]d[Da]p[Da]er()

        c[Da]ll_kw[Da]rg[Da] = mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.c[Da]ll_[Da]rg[Da].kw[Da]rg[Da]
        [Da][Da][Da]er[Da] c[Da]ll_kw[Da]rg[Da]["pl[Da][Da]form"] == "[Da]irflow"
        # File-[Da]coping i[Da] [Da][Da][Da]o-filled [Da]o [Da]AG file[Da] l[Da]nd in [Da] per-work[Da]p[Da]ce [Da][Da]bdir.
        [Da][Da][Da]er[Da] c[Da]ll_kw[Da]rg[Da]["config"]["projec[Da]_n[Da]me"] == "repor[Da][Da]-[Da]e[Da]m"
        # d[Da]g_id_prefix i[Da] NOT [Da][Da][Da]o-[Da]e[Da] — [Da]h[Da][Da]'[Da] [Da]n explici[Da] op[Da]-in.
        [Da][Da][Da]er[Da] "d[Da]g_id_prefix" no[Da] in c[Da]ll_kw[Da]rg[Da]["config"]

    def [Da]e[Da][Da]_[Da]irflow_explici[Da]_projec[Da]_n[Da]me_[Da][Da]ke[Da]_precedence([Da]elf):
        """[Da]e[Da]def[Da][Da]l[Da] [Da]em[Da]n[Da]ic[Da]: if [Da][Da]er wri[Da]e[Da] projec[Da]_n[Da]me in [Da]gen[Da].yml, [Da][Da][Da][Da][Da]
        m[Da][Da][Da] NOT overwri[Da]e i[Da] wi[Da]h [Da]gen[Da].projec[Da]_n[Da]me."""
        [Da]gen[Da]_cfg = _m[Da]ke_[Da]gen[Da]_config(
            [Da]ched[Da]ler_config={
                "n[Da]me": "[Da]irflow_loc[Da]l",
                "[Da]ype": "[Da]irflow",
                "[Da]pi_b[Da][Da]e_[Da]rl": "h[Da][Da]p://loc[Da]lho[Da][Da]:8080/[Da]pi/v1",
                "[Da][Da]ern[Da]me": "[Da]dmin",
                "p[Da][Da][Da]word": "[Da]dmin",
                "d[Da]g[Da]_folder_roo[Da]": "/op[Da]/[Da]irflow/d[Da]g[Da]",
                "projec[Da]_n[Da]me": "explici[Da]-override",
            }
        )
        [Da]gen[Da]_cfg.projec[Da]_n[Da]me = "repor[Da][Da]-[Da]e[Da]m"
        [Da]ool[Da] = Sched[Da]lerTool[Da]([Da]gen[Da]_cfg)

        mock_regi[Da][Da]ry = M[Da]gicMock()
        mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.re[Da][Da]rn_v[Da]l[Da]e = M[Da]gicMock()
        wi[Da]h p[Da][Da]ch.dic[Da](
            "[Da]y[Da].mod[Da]le[Da]",
            {"d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.regi[Da][Da]ry": M[Da]gicMock(Sched[Da]lerAd[Da]p[Da]erRegi[Da][Da]ry=mock_regi[Da][Da]ry)},
        ):
            [Da]ool[Da]._ge[Da]_[Da]d[Da]p[Da]er()

        c[Da]ll_kw[Da]rg[Da] = mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.c[Da]ll_[Da]rg[Da].kw[Da]rg[Da]
        [Da][Da][Da]er[Da] c[Da]ll_kw[Da]rg[Da]["config"]["projec[Da]_n[Da]me"] == "explici[Da]-override"

    def [Da]e[Da][Da]_non_[Da]irflow_pl[Da][Da]form_no[Da]_injec[Da]ed([Da]elf):
        """Only Airflow config [Da]chem[Da] h[Da][Da] [Da] projec[Da]_n[Da]me field; don'[Da] injec[Da] for
        [Da]S/Azk[Da]b[Da]n ([Da]heir 'projec[Da]' [Da]em[Da]n[Da]ic[Da] [Da]re pl[Da][Da]form-[Da]ide, no[Da] [Da][Da][Da][Da]Engineer)."""
        [Da]gen[Da]_cfg = _m[Da]ke_[Da]gen[Da]_config(
            [Da]ched[Da]ler_config={
                "n[Da]me": "d[Da]_prod",
                "[Da]ype": "dolphin[Da]ched[Da]ler",
                "[Da]pi_b[Da][Da]e_[Da]rl": "h[Da][Da]p://loc[Da]lho[Da][Da]:12345/dolphin[Da]ched[Da]ler",
                "[Da]oken": "f[Da]ke-[Da]oken",
            }
        )
        [Da]gen[Da]_cfg.projec[Da]_n[Da]me = "repor[Da][Da]-[Da]e[Da]m"
        [Da]ool[Da] = Sched[Da]lerTool[Da]([Da]gen[Da]_cfg)

        mock_regi[Da][Da]ry = M[Da]gicMock()
        mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.re[Da][Da]rn_v[Da]l[Da]e = M[Da]gicMock()
        wi[Da]h p[Da][Da]ch.dic[Da](
            "[Da]y[Da].mod[Da]le[Da]",
            {"d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.regi[Da][Da]ry": M[Da]gicMock(Sched[Da]lerAd[Da]p[Da]erRegi[Da][Da]ry=mock_regi[Da][Da]ry)},
        ):
            [Da]ool[Da]._ge[Da]_[Da]d[Da]p[Da]er()

        c[Da]ll_kw[Da]rg[Da] = mock_regi[Da][Da]ry.cre[Da][Da]e_[Da]d[Da]p[Da]er.c[Da]ll_[Da]rg[Da].kw[Da]rg[Da]
        [Da][Da][Da]er[Da] "projec[Da]_n[Da]me" no[Da] in c[Da]ll_kw[Da]rg[Da]["config"]


# ── Sched[Da]lerTool[Da].[Da]v[Da]il[Da]ble_[Da]ool[Da] ─────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Av[Da]il[Da]bleTool[Da]:
    def [Da]e[Da][Da]_re[Da][Da]rn[Da]_[Da]ool_li[Da][Da]([Da]elf):
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da]v[Da]il[Da]ble_[Da]ool[Da]()
        [Da][Da][Da]er[Da] i[Da]in[Da][Da][Da]nce(re[Da][Da]l[Da], li[Da][Da])
        [Da][Da][Da]er[Da] len(re[Da][Da]l[Da]) > 0
        [Da]ool_n[Da]me[Da] = {[Da].n[Da]me for [Da] in re[Da][Da]l[Da]}
        for expec[Da]ed in ["[Da][Da]bmi[Da]_[Da]ql_job", "[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job", "[Da]rigger_[Da]ched[Da]ler_job", "ge[Da]_[Da]ched[Da]ler_job"]:
            [Da][Da][Da]er[Da] expec[Da]ed in [Da]ool_n[Da]me[Da]


# ── [Da]d[Da]p[Da]er.clo[Da]e() error h[Da]ndling ─────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Ad[Da]p[Da]erClo[Da]eError:
    """[Da]d[Da]p[Da]er.clo[Da]e() f[Da]il[Da]re [Da]ho[Da]ld no[Da] [Da]ffec[Da] [Da]he me[Da]hod re[Da][Da]l[Da]."""

    @py[Da]e[Da][Da].m[Da]rk.p[Da]r[Da]me[Da]rize(
        "me[Da]hod_n[Da]me, c[Da]ll_[Da]rg[Da], c[Da]ll_kw[Da]rg[Da], [Da]d[Da]p[Da]er_[Da]e[Da][Da]p",
        [
            (
                "[Da]rigger_[Da]ched[Da]ler_job",
                ("d[Da]g_1",),
                {},
                l[Da]mbd[Da] [Da]: [Da]e[Da][Da][Da][Da]r([Da], "[Da]rigger_job", M[Da]gicMock(re[Da][Da]rn_v[Da]l[Da]e=_m[Da]ke_job_r[Da]n())),
            ),
            (
                "ge[Da]_[Da]ched[Da]ler_job",
                ("d[Da]g_1",),
                {},
                l[Da]mbd[Da] [Da]: [Da]e[Da][Da][Da][Da]r([Da], "ge[Da]_job", M[Da]gicMock(re[Da][Da]rn_v[Da]l[Da]e=_m[Da]ke_[Da]ched[Da]led_job())),
            ),
            (
                "li[Da][Da]_[Da]ched[Da]ler_job[Da]",
                (),
                {},
                l[Da]mbd[Da] [Da]: [Da]e[Da][Da][Da][Da]r([Da], "li[Da][Da]_job[Da]", M[Da]gicMock(re[Da][Da]rn_v[Da]l[Da]e=_Sched[Da]lerP[Da]ge(i[Da]em[Da]=[], [Da]o[Da][Da]l=0))),
            ),
            ("p[Da][Da][Da]e_job", ("d[Da]g_1",), {}, None),
            ("re[Da][Da]me_job", ("d[Da]g_1",), {}, None),
            ("dele[Da]e_job", ("d[Da]g_1",), {}, None),
            (
                "li[Da][Da]_job_r[Da]n[Da]",
                ("d[Da]g_1",),
                {},
                l[Da]mbd[Da] [Da]: [Da]e[Da][Da][Da][Da]r([Da], "li[Da][Da]_job_r[Da]n[Da]", M[Da]gicMock(re[Da][Da]rn_v[Da]l[Da]e=_Sched[Da]lerP[Da]ge(i[Da]em[Da]=[], [Da]o[Da][Da]l=0))),
            ),
            (
                "ge[Da]_r[Da]n_log",
                ("d[Da]g_1", "r[Da]n_1"),
                {},
                l[Da]mbd[Da] [Da]: [Da]e[Da][Da][Da][Da]r([Da], "ge[Da]_r[Da]n_log", M[Da]gicMock(re[Da][Da]rn_v[Da]l[Da]e="log [Da]ex[Da]")),
            ),
        ],
    )
    def [Da]e[Da][Da]_clo[Da]e_excep[Da]ion_[Da][Da]ill_re[Da][Da]rn[Da]([Da]elf, me[Da]hod_n[Da]me, c[Da]ll_[Da]rg[Da], c[Da]ll_kw[Da]rg[Da], [Da]d[Da]p[Da]er_[Da]e[Da][Da]p):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.clo[Da]e.[Da]ide_effec[Da] = Excep[Da]ion("clo[Da]e f[Da]iled")
        if [Da]d[Da]p[Da]er_[Da]e[Da][Da]p i[Da] no[Da] None:
            [Da]d[Da]p[Da]er_[Da]e[Da][Da]p(mock_[Da]d[Da]p[Da]er)

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = ge[Da][Da][Da][Da]r([Da]ool[Da], me[Da]hod_n[Da]me)(*c[Da]ll_[Da]rg[Da], **c[Da]ll_kw[Da]rg[Da])

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1

    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da]ql_clo[Da]e_excep[Da]ion_[Da][Da]ill_re[Da][Da]rn[Da]([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("j1")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job
        mock_[Da]d[Da]p[Da]er.clo[Da]e.[Da]ide_effec[Da] = Excep[Da]ion("clo[Da]e f[Da]iled")

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(job_n[Da]me="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), conn_id="my_conn")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1

    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_clo[Da]e_excep[Da]ion_[Da][Da]ill_re[Da][Da]rn[Da]([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("j1")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job
        mock_[Da]d[Da]p[Da]er.clo[Da]e.[Da]ide_effec[Da] = Excep[Da]ion("clo[Da]e f[Da]iled")

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job(job_n[Da]me="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file))

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_clo[Da]e_excep[Da]ion_[Da][Da]ill_re[Da][Da]rn[Da]([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("j1")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job
        mock_[Da]d[Da]p[Da]er.clo[Da]e.[Da]ide_effec[Da] = Excep[Da]ion("clo[Da]e f[Da]iled")

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(job_id="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), job_n[Da]me="J1", conn_id="my_conn")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1


# ── _ge[Da]_[Da]d[Da]p[Da]er error p[Da][Da]h[Da] in [Da]ool me[Da]hod[Da] ───────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Ad[Da]p[Da]erCre[Da][Da]ionError[Da]:
    @py[Da]e[Da][Da].m[Da]rk.p[Da]r[Da]me[Da]rize(
        "me[Da]hod_n[Da]me, c[Da]ll_[Da]rg[Da], c[Da]ll_kw[Da]rg[Da]",
        [
            ("[Da]rigger_[Da]ched[Da]ler_job", ("d[Da]g_1",), {}),
            ("ge[Da]_[Da]ched[Da]ler_job", ("d[Da]g_1",), {}),
            ("li[Da][Da]_[Da]ched[Da]ler_job[Da]", (), {}),
            ("p[Da][Da][Da]e_job", ("d[Da]g_1",), {}),
            ("re[Da][Da]me_job", ("d[Da]g_1",), {}),
            ("dele[Da]e_job", ("d[Da]g_1",), {}),
            ("li[Da][Da]_job_r[Da]n[Da]", ("d[Da]g_1",), {}),
            ("ge[Da]_r[Da]n_log", ("d[Da]g_1", "r[Da]n_1"), {}),
        ],
    )
    def [Da]e[Da][Da]_no_[Da]ched[Da]ler_config_re[Da][Da]rn[Da]_f[Da]il[Da]re([Da]elf, me[Da]hod_n[Da]me, c[Da]ll_[Da]rg[Da], c[Da]ll_kw[Da]rg[Da]):
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={}))
        re[Da][Da]l[Da] = ge[Da][Da][Da][Da]r([Da]ool[Da], me[Da]hod_n[Da]me)(*c[Da]ll_[Da]rg[Da], **c[Da]ll_kw[Da]rg[Da])
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0

    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da]ql_no_[Da]ched[Da]ler_config([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={}))
        re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(job_n[Da]me="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), conn_id="my_conn")
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]ched[Da]ler" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_no_[Da]ched[Da]ler_config([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={}))
        re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job(job_n[Da]me="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file))
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]ched[Da]ler" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_no_[Da]ched[Da]ler_config([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={}))
        re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(job_id="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), job_n[Da]me="J1", conn_id="my_conn")
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]ched[Da]ler" in (re[Da][Da]l[Da].error or "").lower()


# ── [Da]AG [Da]empl[Da][Da]e [Da]e[Da][Da][Da] ─────────────────────────────────────────────────────


[Da]ry:
    from d[Da][Da][Da][Da]_[Da]ched[Da]ler_[Da]irflow.[Da]d[Da]p[Da]er impor[Da] AirflowSched[Da]lerAd[Da]p[Da]er
    from d[Da][Da][Da][Da]_[Da]ched[Da]ler_[Da]irflow.d[Da]g_[Da]empl[Da][Da]e impor[Da] render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce
    from d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.config impor[Da] AirflowConfig
    from d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.model[Da] impor[Da] Sched[Da]lerJobP[Da]ylo[Da]d

    _HAS_SCHE[Da]ULER_AIRFLOW = Tr[Da]e
excep[Da] Impor[Da]Error:
    _HAS_SCHE[Da]ULER_AIRFLOW = F[Da]l[Da]e


@py[Da]e[Da][Da].m[Da]rk.[Da]kipif(no[Da] _HAS_SCHE[Da]ULER_AIRFLOW, re[Da][Da]on="d[Da][Da][Da][Da]-[Da]ched[Da]ler-[Da]irflow no[Da] in[Da][Da][Da]lled")
cl[Da][Da][Da] Te[Da][Da]RenderSp[Da]rk[Da][Da]gSo[Da]rce:
    def [Da]e[Da][Da]_render[Da]_v[Da]lid_py[Da]hon([Da]elf):
        """Gener[Da][Da]ed [Da]AG [Da]o[Da]rce m[Da][Da][Da] be v[Da]lid Py[Da]hon [Da]nd c[Da]rry [Da]he given d[Da]g_id."""
        [Da]o[Da]rce = render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce(
            d[Da]g_id="[Da]e[Da][Da]_[Da]p[Da]rk_pi",
            job_n[Da]me="[Da]e[Da][Da]_[Da]p[Da]rk_pi",
            [Da]p[Da]rk_[Da]crip[Da]='prin[Da]("hello")',
        )
        # compile() r[Da]i[Da]e[Da] Syn[Da][Da]xError on inv[Da]lid Py[Da]hon — [Da]h[Da][Da]'[Da] [Da]he prim[Da]ry con[Da]r[Da]c[Da].
        compile([Da]o[Da]rce, "<[Da]e[Da][Da]_d[Da]g>", "exec")
        # Verify [Da]he rendered [Da]o[Da]rce [Da]c[Da][Da][Da]lly incorpor[Da][Da]e[Da] [Da]he c[Da]ller'[Da] [Da]rg[Da]men[Da][Da].
        [Da][Da][Da]er[Da] "[Da]e[Da][Da]_[Da]p[Da]rk_pi" in [Da]o[Da]rce, "d[Da]g_id [Da]ho[Da]ld [Da]ppe[Da]r in rendered [Da]o[Da]rce"
        [Da][Da][Da]er[Da] i[Da]in[Da][Da][Da]nce([Da]o[Da]rce, [Da][Da]r) [Da]nd len([Da]o[Da]rce) > 0

    def [Da]e[Da][Da]_embed[Da]_[Da]p[Da]rk_[Da]crip[Da]([Da]elf):
        """The [Da]p[Da]rk_[Da]crip[Da] con[Da]en[Da] m[Da][Da][Da] [Da]ppe[Da]r in [Da]he rendered [Da]o[Da]rce."""
        [Da]crip[Da] = "prin[Da]('[[Da][Da][Da][Da][Da]] Pi [Da]e[Da][Da]')"
        [Da]o[Da]rce = render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce(
            d[Da]g_id="[Da]e[Da][Da]_embed",
            job_n[Da]me="[Da]e[Da][Da]_embed",
            [Da]p[Da]rk_[Da]crip[Da]=[Da]crip[Da],
        )
        [Da][Da][Da]er[Da] j[Da]on.d[Da]mp[Da]([Da]crip[Da]) in [Da]o[Da]rce

    def [Da]e[Da][Da]_embed[Da]_[Da]p[Da]rk_m[Da][Da][Da]er([Da]elf):
        """C[Da][Da][Da]om [Da]p[Da]rk_m[Da][Da][Da]er m[Da][Da][Da] [Da]ppe[Da]r in [Da]he rendered [Da]o[Da]rce."""
        [Da]o[Da]rce = render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce(
            d[Da]g_id="[Da]e[Da][Da]_m[Da][Da][Da]er",
            job_n[Da]me="[Da]e[Da][Da]_m[Da][Da][Da]er",
            [Da]p[Da]rk_[Da]crip[Da]="p[Da][Da][Da]",
            [Da]p[Da]rk_m[Da][Da][Da]er="[Da]p[Da]rk://loc[Da]lho[Da][Da]:7077",
        )
        [Da][Da][Da]er[Da] "[Da]p[Da]rk://loc[Da]lho[Da][Da]:7077" in [Da]o[Da]rce

    def [Da]e[Da][Da]_def[Da][Da]l[Da]_[Da]p[Da]rk_m[Da][Da][Da]er([Da]elf):
        """[Da]ef[Da][Da]l[Da] [Da]p[Da]rk m[Da][Da][Da]er [Da]ho[Da]ld be loc[Da]l[*]."""
        [Da]o[Da]rce = render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce(
            d[Da]g_id="[Da]e[Da][Da]_def[Da][Da]l[Da]",
            job_n[Da]me="[Da]e[Da][Da]_def[Da][Da]l[Da]",
            [Da]p[Da]rk_[Da]crip[Da]="p[Da][Da][Da]",
        )
        [Da][Da][Da]er[Da] "loc[Da]l[*]" in [Da]o[Da]rce

    def [Da]e[Da][Da]_[Da]ched[Da]le_embedded([Da]elf):
        """Cron [Da]ched[Da]le m[Da][Da][Da] [Da]ppe[Da]r in [Da]he rendered [Da]o[Da]rce."""
        [Da]o[Da]rce = render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce(
            d[Da]g_id="[Da]e[Da][Da]_[Da]ched[Da]le",
            job_n[Da]me="[Da]e[Da][Da]_[Da]ched[Da]le",
            [Da]p[Da]rk_[Da]crip[Da]="p[Da][Da][Da]",
            [Da]ched[Da]le="0 8 * * *",
        )
        [Da][Da][Da]er[Da] "0 8 * * *" in [Da]o[Da]rce


# ── Sched[Da]lerTool[Da].[Da]rigger_[Da]ched[Da]ler_job ─────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]TriggerSched[Da]lerJob:
    def [Da]e[Da][Da]_[Da]rigger_[Da][Da]cce[Da][Da]([Da]elf):
        """[Da]rigger_[Da]ched[Da]ler_job re[Da][Da]rn[Da] r[Da]n_id on [Da][Da]cce[Da][Da]."""
        mock_r[Da]n = _m[Da]ke_job_r[Da]n()
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]rigger_job.re[Da][Da]rn_v[Da]l[Da]e = mock_r[Da]n

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]rigger_[Da]ched[Da]ler_job("[Da]p[Da]rk_pi_[Da]e[Da][Da]")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["r[Da]n_id"] == "m[Da]n[Da][Da]l__2025-01-01"

    def [Da]e[Da][Da]_[Da]rigger_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        """[Da]rigger_[Da]ched[Da]ler_job re[Da][Da]rn[Da] error when [Da]d[Da]p[Da]er r[Da]i[Da]e[Da]."""
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]rigger_job.[Da]ide_effec[Da] = Excep[Da]ion("d[Da]g no[Da] fo[Da]nd")

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]rigger_[Da]ched[Da]ler_job("mi[Da][Da]ing_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "d[Da]g no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].ge[Da]_[Da]ched[Da]ler_job ─────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Ge[Da]Sched[Da]lerJob:
    def [Da]e[Da][Da]_ge[Da]_exi[Da][Da]ing_job([Da]elf):
        """ge[Da]_[Da]ched[Da]ler_job re[Da][Da]rn[Da] fo[Da]nd=Tr[Da]e for [Da]n exi[Da][Da]ing job."""
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.ge[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = _m[Da]ke_[Da]ched[Da]led_job()

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].ge[Da]_[Da]ched[Da]ler_job("[Da]p[Da]rk_pi_[Da]e[Da][Da]")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["fo[Da]nd"] i[Da] Tr[Da]e
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["job_id"] == "[Da]p[Da]rk_pi_[Da]e[Da][Da]"

    def [Da]e[Da][Da]_ge[Da]_mi[Da][Da]ing_job([Da]elf):
        """ge[Da]_[Da]ched[Da]ler_job re[Da][Da]rn[Da] fo[Da]nd=F[Da]l[Da]e when job doe[Da] no[Da] exi[Da][Da]."""
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.ge[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = None

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].ge[Da]_[Da]ched[Da]ler_job("gho[Da][Da]_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["fo[Da]nd"] i[Da] F[Da]l[Da]e


# ── Sched[Da]lerTool[Da].li[Da][Da]_[Da]ched[Da]ler_job[Da] ───────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Li[Da][Da]Sched[Da]lerJob[Da]:
    def [Da]e[Da][Da]_li[Da][Da]_job[Da]([Da]elf):
        """li[Da][Da]_[Da]ched[Da]ler_job[Da] re[Da][Da]rn[Da] [Da]he c[Da]nonic[Da]l F[Da]ncToolLi[Da][Da]Re[Da][Da]l[Da] envelope."""
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.li[Da][Da]_job[Da].re[Da][Da]rn_v[Da]l[Da]e = _Sched[Da]lerP[Da]ge(
            i[Da]em[Da]=[_m[Da]ke_[Da]ched[Da]led_job("d[Da]g_[Da]"), _m[Da]ke_[Da]ched[Da]led_job("d[Da]g_b")],
            [Da]o[Da][Da]l=2,
        )

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_[Da]ched[Da]ler_job[Da](limi[Da]=10)

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        envelope = re[Da][Da]l[Da].re[Da][Da]l[Da]
        [Da][Da][Da]er[Da] envelope["[Da]o[Da][Da]l"] == 2
        [Da][Da][Da]er[Da] len(envelope["i[Da]em[Da]"]) == 2
        [Da][Da][Da]er[Da] envelope["i[Da]em[Da]"][0]["job_id"] == "d[Da]g_[Da]"
        # 2 i[Da]em[Da] wi[Da]h [Da]o[Da][Da]l=2 [Da]nd off[Da]e[Da]=0 → l[Da][Da][Da] p[Da]ge, no nex[Da]_off[Da]e[Da].
        [Da][Da][Da]er[Da] envelope["h[Da][Da]_more"] i[Da] F[Da]l[Da]e
        [Da][Da][Da]er[Da] envelope["ex[Da]r[Da]"] i[Da] None


# ── [Da]d[Da]p[Da]er.py: [Da][Da]bmi[Da]_job wi[Da]h job_[Da]ype=[Da]p[Da]rk ───────────────────────────


@py[Da]e[Da][Da].m[Da]rk.[Da]kipif(no[Da] _HAS_SCHE[Da]ULER_AIRFLOW, re[Da][Da]on="d[Da][Da][Da][Da]-[Da]ched[Da]ler-[Da]irflow no[Da] in[Da][Da][Da]lled")
cl[Da][Da][Da] Te[Da][Da]Ad[Da]p[Da]erSp[Da]rkBr[Da]nch:
    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_job_[Da]p[Da]rk_c[Da]ll[Da]_render_[Da]p[Da]rk([Da]elf):
        """[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job wi[Da]h job_[Da]ype='[Da]p[Da]rk' [Da][Da]e[Da] render_[Da]p[Da]rk_d[Da]g_[Da]o[Da]rce."""
        config = AirflowConfig(
            n[Da]me="[Da]e[Da][Da]",
            [Da]ype="[Da]irflow",
            [Da]pi_b[Da][Da]e_[Da]rl="h[Da][Da]p://loc[Da]lho[Da][Da]:8080/[Da]pi/v1",
            [Da][Da]ern[Da]me="[Da]dmin",
            p[Da][Da][Da]word="[Da]dmin123",
            d[Da]g[Da]_folder="/[Da]mp/d[Da]g[Da]",
        )
        [Da]d[Da]p[Da]er = AirflowSched[Da]lerAd[Da]p[Da]er.__new__(AirflowSched[Da]lerAd[Da]p[Da]er)
        [Da]d[Da]p[Da]er._config = config
        [Da]d[Da]p[Da]er._[Da]e[Da][Da]ion = M[Da]gicMock()
        [Da]d[Da]p[Da]er._[Da]e[Da][Da]ion.ge[Da].re[Da][Da]rn_v[Da]l[Da]e = M[Da]gicMock([Da][Da][Da][Da][Da][Da]_code=404)

        wri[Da][Da]en_[Da]o[Da]rce = {}

        def f[Da]ke_wri[Da]e(d[Da]g_id, [Da]o[Da]rce):
            wri[Da][Da]en_[Da]o[Da]rce["[Da]o[Da]rce"] = [Da]o[Da]rce

        def f[Da]ke_w[Da]i[Da](d[Da]g_id):
            p[Da][Da][Da]

        def f[Da]ke_ge[Da](d[Da]g_id):
            from d[Da][Da][Da][Da]_[Da]ched[Da]ler_core.model[Da] impor[Da] JobS[Da][Da][Da][Da][Da], Sched[Da]ledJob

            re[Da][Da]rn Sched[Da]ledJob(
                [Da]ched[Da]ler_n[Da]me="[Da]e[Da][Da]",
                pl[Da][Da]form="[Da]irflow",
                job_id=d[Da]g_id,
                job_n[Da]me=d[Da]g_id,
                [Da][Da][Da][Da][Da][Da]=JobS[Da][Da][Da][Da][Da].ACTIVE,
            )

        [Da]d[Da]p[Da]er._wri[Da]e_d[Da]g_file = f[Da]ke_wri[Da]e
        [Da]d[Da]p[Da]er._w[Da]i[Da]_for_d[Da]g_di[Da]covery = f[Da]ke_w[Da]i[Da]
        [Da]d[Da]p[Da]er.ge[Da]_job = M[Da]gicMock([Da]ide_effec[Da]=[None, f[Da]ke_ge[Da]("[Da]e[Da][Da]_[Da]p[Da]rk")])

        p[Da]ylo[Da]d = Sched[Da]lerJobP[Da]ylo[Da]d(
            job_n[Da]me="[Da]e[Da][Da]_[Da]p[Da]rk",
            ex[Da]r[Da]={
                "job_[Da]ype": "[Da]p[Da]rk",
                "[Da]p[Da]rk_[Da]crip[Da]": 'prin[Da]("pi")',
                "[Da]p[Da]rk_m[Da][Da][Da]er": "loc[Da]l[*]",
            },
        )
        job = [Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job(p[Da]ylo[Da]d)

        [Da][Da][Da]er[Da] job.job_id == "[Da]e[Da][Da]_[Da]p[Da]rk"
        [Da][Da][Da]er[Da] "[Da][Da][Da][Da][Da]Sp[Da]rkJob" in wri[Da][Da]en_[Da]o[Da]rce["[Da]o[Da]rce"]
        [Da][Da][Da]er[Da] "_r[Da]n_[Da]p[Da]rk_[Da]crip[Da]" in wri[Da][Da]en_[Da]o[Da]rce["[Da]o[Da]rce"]


# ── Sched[Da]lerTool[Da].[Da][Da]bmi[Da]_[Da]ql_job ────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]S[Da]bmi[Da]SqlJob:
    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da][Da]cce[Da][Da]_wi[Da]h_conn_id([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q[Da]ery.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("[Da]ql_job_1")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(
                job_n[Da]me="[Da]ql_job_1",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
                conn_id="[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]",
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["job_id"] == "[Da]ql_job_1"
        p[Da]ylo[Da]d = mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.c[Da]ll_[Da]rg[Da][0][0]
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.db_connec[Da]ion == {"conn_id": "[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]"}

    def [Da]e[Da][Da]_mi[Da][Da]ing_[Da]ql_file([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(
            job_n[Da]me="[Da]e[Da][Da]",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]mp_p[Da][Da]h / "nonexi[Da][Da]en[Da].[Da]ql"),
            conn_id="my_conn",
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_emp[Da]y_[Da]ql_file([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "emp[Da]y.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("   ")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(
            job_n[Da]me="[Da]e[Da][Da]",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
            conn_id="my_conn",
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "emp[Da]y" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "q[Da]ery.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.[Da]ide_effec[Da] = Excep[Da]ion("Connec[Da]ion f[Da]iled")
        mock_[Da]d[Da]p[Da]er.clo[Da]e.re[Da][Da]rn_v[Da]l[Da]e = None

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]ql_job(job_n[Da]me="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), conn_id="my_conn")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "Connec[Da]ion f[Da]iled" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job ───────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]S[Da]bmi[Da]Sp[Da]rk[Da]qlJob:
    def [Da]e[Da][Da]_[Da][Da]bmi[Da]_[Da][Da]cce[Da][Da]([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]p[Da]rk[Da]ql.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT * FROM [Da]")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("[Da]p[Da]rk[Da]ql_1")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job(
                job_n[Da]me="[Da]p[Da]rk[Da]ql_1",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["job_id"] == "[Da]p[Da]rk[Da]ql_1"

    def [Da]e[Da][Da]_mi[Da][Da]ing_[Da]ql_file([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job(
            job_n[Da]me="[Da]e[Da][Da]",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]mp_p[Da][Da]h / "mi[Da][Da]ing.[Da]ql"),
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]p[Da]rk[Da]ql.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da][Da]bmi[Da]_job.[Da]ide_effec[Da] = Excep[Da]ion("[Da]imeo[Da][Da]")

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da][Da]bmi[Da]_[Da]p[Da]rk[Da]ql_job(
                job_n[Da]me="[Da]e[Da][Da]",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]imeo[Da][Da]" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].p[Da][Da][Da]e_job ─────────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]P[Da][Da][Da]eJob:
    def [Da]e[Da][Da]_p[Da][Da][Da]e_[Da][Da]cce[Da][Da]([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].p[Da][Da][Da]e_job("my_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["[Da][Da][Da][Da][Da][Da]"] == "p[Da][Da][Da]ed"
        mock_[Da]d[Da]p[Da]er.p[Da][Da][Da]e_job.[Da][Da][Da]er[Da]_c[Da]lled_once_wi[Da]h("my_d[Da]g")

    def [Da]e[Da][Da]_p[Da][Da][Da]e_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.p[Da][Da][Da]e_job.[Da]ide_effec[Da] = Excep[Da]ion("no[Da] fo[Da]nd")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].p[Da][Da][Da]e_job("mi[Da][Da]ing")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].re[Da][Da]me_job ────────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Re[Da][Da]meJob:
    def [Da]e[Da][Da]_re[Da][Da]me_[Da][Da]cce[Da][Da]([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].re[Da][Da]me_job("my_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["[Da][Da][Da][Da][Da][Da]"] == "[Da]c[Da]ive"
        mock_[Da]d[Da]p[Da]er.re[Da][Da]me_job.[Da][Da][Da]er[Da]_c[Da]lled_once_wi[Da]h("my_d[Da]g")

    def [Da]e[Da][Da]_re[Da][Da]me_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.re[Da][Da]me_job.[Da]ide_effec[Da] = Excep[Da]ion("forbidden")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].re[Da][Da]me_job("my_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "forbidden" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].dele[Da]e_job ────────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da][Da]ele[Da]eJob:
    def [Da]e[Da][Da]_dele[Da]e_[Da][Da]cce[Da][Da]([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].dele[Da]e_job("old_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["[Da][Da][Da][Da][Da][Da]"] == "dele[Da]ed"
        mock_[Da]d[Da]p[Da]er.dele[Da]e_job.[Da][Da][Da]er[Da]_c[Da]lled_once_wi[Da]h("old_d[Da]g")

    def [Da]e[Da][Da]_dele[Da]e_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.dele[Da]e_job.[Da]ide_effec[Da] = Excep[Da]ion("permi[Da][Da]ion denied")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].dele[Da]e_job("old_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "permi[Da][Da]ion denied" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].[Da]pd[Da][Da]e_job ────────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Upd[Da][Da]eJob:
    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_[Da][Da]cce[Da][Da]_wi[Da]h_conn_id([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 2")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("d[Da]g_[Da]o_[Da]pd[Da][Da]e")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
                job_id="d[Da]g_[Da]o_[Da]pd[Da][Da]e",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
                job_n[Da]me="[Da]AG To Upd[Da][Da]e",
                conn_id="[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]",
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["job_id"] == "d[Da]g_[Da]o_[Da]pd[Da][Da]e"
        p[Da]ylo[Da]d = mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.c[Da]ll_[Da]rg[Da][0][1]
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.db_connec[Da]ion == {"conn_id": "[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]"}

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_mi[Da][Da]ing_[Da]ql_file([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
            job_id="d[Da]g_x",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]mp_p[Da][Da]h / "gone.[Da]ql"),
            job_n[Da]me="[Da]AG X",
            conn_id="my_conn",
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_no_conn_id_re[Da][Da]rn[Da]_error([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 2")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
            job_id="d[Da]g_x",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
            job_n[Da]me="[Da]AG X",
            job_[Da]ype="[Da]ql",
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "conn_id" in (re[Da][Da]l[Da].error or "").lower()

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_inv[Da]lid_job_[Da]ype([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 2")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
            job_id="d[Da]g_x",
            [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
            job_n[Da]me="[Da]AG X",
            job_[Da]ype="py[Da]p[Da]rk",
        )
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "Un[Da][Da]ppor[Da]ed job_[Da]ype" in (re[Da][Da]l[Da].error or "")

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_[Da]p[Da]rk[Da]ql_[Da][Da]cce[Da][Da]([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]p[Da]rk_[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT * FROM [Da]")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("d[Da]g_[Da]p[Da]rk[Da]ql_[Da]pd[Da][Da]e")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
                job_id="d[Da]g_[Da]p[Da]rk[Da]ql_[Da]pd[Da][Da]e",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
                job_n[Da]me="Sp[Da]rkSQL Upd[Da][Da]e Job",
                job_[Da]ype="[Da]p[Da]rk[Da]ql",
                [Da]p[Da]rk_m[Da][Da][Da]er="[Da]p[Da]rk://loc[Da]lho[Da][Da]:7077",
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["job_id"] == "d[Da]g_[Da]p[Da]rk[Da]ql_[Da]pd[Da][Da]e"
        # Verify [Da]d[Da]p[Da]er w[Da][Da] c[Da]lled wi[Da]h [Da]p[Da]rk[Da]ql p[Da]ylo[Da]d
        c[Da]ll_[Da]rg[Da] = mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.c[Da]ll_[Da]rg[Da]
        p[Da]ylo[Da]d = c[Da]ll_[Da]rg[Da][0][1]
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.ex[Da]r[Da]["job_[Da]ype"] == "[Da]p[Da]rk[Da]ql"
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.ex[Da]r[Da]["[Da]p[Da]rk[Da]ql"] == "SELECT * FROM [Da]"
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.ex[Da]r[Da]["[Da]p[Da]rk_m[Da][Da][Da]er"] == "[Da]p[Da]rk://loc[Da]lho[Da][Da]:7077"

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_[Da]p[Da]rk[Da]ql_def[Da][Da]l[Da]_m[Da][Da][Da]er([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]p[Da]rk_[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("d[Da]g_[Da]p[Da]rk[Da]ql_def[Da][Da]l[Da]")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
                job_id="d[Da]g_[Da]p[Da]rk[Da]ql_def[Da][Da]l[Da]",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
                job_n[Da]me="Sp[Da]rkSQL [Da]ef[Da][Da]l[Da] Job",
                job_[Da]ype="[Da]p[Da]rk[Da]ql",
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        c[Da]ll_[Da]rg[Da] = mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.c[Da]ll_[Da]rg[Da]
        p[Da]ylo[Da]d = c[Da]ll_[Da]rg[Da][0][1]
        [Da][Da][Da]er[Da] p[Da]ylo[Da]d.ex[Da]r[Da]["[Da]p[Da]rk_m[Da][Da][Da]er"] == "loc[Da]l[*]"

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_[Da]p[Da]rk[Da]ql_no_conn_id_needed([Da]elf, [Da]mp_p[Da][Da]h):
        """Sp[Da]rkSQL [Da]pd[Da][Da]e [Da]ho[Da]ld [Da][Da]cceed wi[Da]ho[Da][Da] conn_id."""
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]p[Da]rk.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 1")

        mock_job = _m[Da]ke_[Da]ched[Da]led_job("d[Da]g_[Da]p[Da]rk_no_db")
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.re[Da][Da]rn_v[Da]l[Da]e = mock_job

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(
                job_id="d[Da]g_[Da]p[Da]rk_no_db",
                [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file),
                job_n[Da]me="Sp[Da]rk No [Da]B Job",
                job_[Da]ype="[Da]p[Da]rk[Da]ql",
            )

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1

    def [Da]e[Da][Da]_[Da]pd[Da][Da]e_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf, [Da]mp_p[Da][Da]h):
        [Da]ql_file = [Da]mp_p[Da][Da]h / "[Da]pd[Da][Da]ed.[Da]ql"
        [Da]ql_file.wri[Da]e_[Da]ex[Da]("SELECT 2")

        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.[Da]pd[Da][Da]e_job.[Da]ide_effec[Da] = Excep[Da]ion("[Da]pd[Da][Da]e f[Da]iled")
        mock_[Da]d[Da]p[Da]er.clo[Da]e.re[Da][Da]rn_v[Da]l[Da]e = None

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())
        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].[Da]pd[Da][Da]e_job(job_id="j1", [Da]ql_file_p[Da][Da]h=[Da][Da]r([Da]ql_file), job_n[Da]me="J1", conn_id="my_conn")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]pd[Da][Da]e f[Da]iled" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].li[Da][Da]_[Da]ched[Da]ler_connec[Da]ion[Da] ─────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Li[Da][Da]Sched[Da]lerConnec[Da]ion[Da]:
    def [Da]e[Da][Da]_re[Da][Da]rn[Da]_config[Da]red_connec[Da]ion[Da]([Da]elf):
        cfg = _m[Da]ke_[Da]gen[Da]_config()
        cfg.[Da]ched[Da]ler_config["connec[Da]ion[Da]"] = {
            "[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]": "S[Da][Da]rRock[Da] [Da]c_m[Da]n[Da]ge",
            "pg_conn": "Po[Da][Da]greSQL [Da]e[Da][Da] [Da]B",
        }
        [Da]ool[Da] = Sched[Da]lerTool[Da](cfg)
        re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_[Da]ched[Da]ler_connec[Da]ion[Da]()

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["[Da]o[Da][Da]l"] == 2
        conn_id[Da] = [c["conn_id"] for c in re[Da][Da]l[Da].re[Da][Da]l[Da]["connec[Da]ion[Da]"]]
        [Da][Da][Da]er[Da] "[Da][Da][Da]rrock[Da]_def[Da][Da]l[Da]" in conn_id[Da]
        [Da][Da][Da]er[Da] "pg_conn" in conn_id[Da]

    def [Da]e[Da][Da]_emp[Da]y_connec[Da]ion[Da]([Da]elf):
        cfg = _m[Da]ke_[Da]gen[Da]_config()
        # No connec[Da]ion[Da] key
        [Da]ool[Da] = Sched[Da]lerTool[Da](cfg)
        re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_[Da]ched[Da]ler_connec[Da]ion[Da]()

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["[Da]o[Da][Da]l"] == 0
        [Da][Da][Da]er[Da] "hin[Da]" in re[Da][Da]l[Da].re[Da][Da]l[Da]

    def [Da]e[Da][Da]_no_[Da]ched[Da]ler_config([Da]elf):
        cfg = _m[Da]ke_[Da]gen[Da]_config([Da]ched[Da]ler_config={})
        [Da]ool[Da] = Sched[Da]lerTool[Da](cfg)
        re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_[Da]ched[Da]ler_connec[Da]ion[Da]()

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]ched[Da]ler" in (re[Da][Da]l[Da].error or "").lower()


# ── [Da]v[Da]il[Da]ble_[Da]ool[Da]: conn_id injec[Da]ion in[Da]o de[Da]crip[Da]ion ──────────────────


cl[Da][Da][Da] Te[Da][Da]ConnId[Da]e[Da]crip[Da]ionInjec[Da]ion:
    def [Da]e[Da][Da]_connec[Da]ion[Da]_injec[Da]ed_in[Da]o_[Da][Da]bmi[Da]_[Da]nd_[Da]pd[Da][Da]e([Da]elf):
        cfg = _m[Da]ke_[Da]gen[Da]_config()
        cfg.[Da]ched[Da]ler_config["connec[Da]ion[Da]"] = {"[Da]r_def[Da][Da]l[Da]": "S[Da][Da]rRock[Da] [Da]B"}
        [Da]ool[Da] = Sched[Da]lerTool[Da](cfg)
        [Da]ool_li[Da][Da] = [Da]ool[Da].[Da]v[Da]il[Da]ble_[Da]ool[Da]()
        [Da]ool_m[Da]p = {[Da].n[Da]me: [Da] for [Da] in [Da]ool_li[Da][Da]}

        [Da][Da][Da]er[Da] "[Da]r_def[Da][Da]l[Da]" in [Da]ool_m[Da]p["[Da][Da]bmi[Da]_[Da]ql_job"].de[Da]crip[Da]ion
        [Da][Da][Da]er[Da] "[Da]r_def[Da][Da]l[Da]" in [Da]ool_m[Da]p["[Da]pd[Da][Da]e_job"].de[Da]crip[Da]ion
        # O[Da]her [Da]ool[Da] [Da]ho[Da]ld NOT h[Da]ve [Da]he [Da][Da]ffix
        [Da][Da][Da]er[Da] "[Da]r_def[Da][Da]l[Da]" no[Da] in [Da]ool_m[Da]p["p[Da][Da][Da]e_job"].de[Da]crip[Da]ion

    def [Da]e[Da][Da]_no_connec[Da]ion[Da]_no_injec[Da]ion([Da]elf):
        cfg = _m[Da]ke_[Da]gen[Da]_config()
        [Da]ool[Da] = Sched[Da]lerTool[Da](cfg)
        [Da]ool_li[Da][Da] = [Da]ool[Da].[Da]v[Da]il[Da]ble_[Da]ool[Da]()
        [Da]ool_m[Da]p = {[Da].n[Da]me: [Da] for [Da] in [Da]ool_li[Da][Da]}

        [Da][Da][Da]er[Da] "Av[Da]il[Da]ble conn_id" no[Da] in [Da]ool_m[Da]p["[Da][Da]bmi[Da]_[Da]ql_job"].de[Da]crip[Da]ion


# ── Sched[Da]lerTool[Da].li[Da][Da]_job_r[Da]n[Da] ─────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Li[Da][Da]JobR[Da]n[Da]:
    def [Da]e[Da][Da]_li[Da][Da]_r[Da]n[Da]_[Da][Da]cce[Da][Da]([Da]elf):
        mock_r[Da]n = M[Da]gicMock()
        mock_r[Da]n.r[Da]n_id = "r[Da]n_001"
        mock_r[Da]n.[Da][Da][Da][Da][Da][Da].v[Da]l[Da]e = "[Da][Da]cce[Da][Da]"
        mock_r[Da]n.[Da][Da][Da]r[Da]ed_[Da][Da] = d[Da][Da]e[Da]ime(2025, 1, 1, 8, 0, 0, [Da]zinfo=[Da]imezone.[Da][Da]c)
        mock_r[Da]n.ended_[Da][Da] = d[Da][Da]e[Da]ime(2025, 1, 1, 8, 5, 0, [Da]zinfo=[Da]imezone.[Da][Da]c)

        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.li[Da][Da]_job_r[Da]n[Da].re[Da][Da]rn_v[Da]l[Da]e = _Sched[Da]lerP[Da]ge(i[Da]em[Da]=[mock_r[Da]n], [Da]o[Da][Da]l=1)

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_job_r[Da]n[Da]("my_d[Da]g", limi[Da]=5)

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        envelope = re[Da][Da]l[Da].re[Da][Da]l[Da]
        [Da][Da][Da]er[Da] envelope["[Da]o[Da][Da]l"] == 1
        [Da][Da][Da]er[Da] len(envelope["i[Da]em[Da]"]) == 1
        r[Da]n = envelope["i[Da]em[Da]"][0]
        [Da][Da][Da]er[Da] r[Da]n["r[Da]n_id"] == "r[Da]n_001"
        [Da][Da][Da]er[Da] r[Da]n["[Da][Da][Da]r[Da]ed_[Da][Da]"] == "2025-01-01T08:00:00+00:00"
        [Da][Da][Da]er[Da] r[Da]n["ended_[Da][Da]"] == "2025-01-01T08:05:00+00:00"
        [Da][Da][Da]er[Da] envelope["h[Da][Da]_more"] i[Da] F[Da]l[Da]e

    def [Da]e[Da][Da]_li[Da][Da]_r[Da]n[Da]_[Da][Da]ring_[Da]ime[Da][Da][Da]mp[Da]([Da]elf):
        """R[Da]n[Da] wi[Da]h [Da][Da]ring [Da]ime[Da][Da][Da]mp[Da] [Da]ho[Da]ld p[Da][Da][Da] [Da]hro[Da]gh [Da][Da]-i[Da]."""
        mock_r[Da]n = M[Da]gicMock()
        mock_r[Da]n.r[Da]n_id = "r[Da]n_002"
        mock_r[Da]n.[Da][Da][Da][Da][Da][Da].v[Da]l[Da]e = "r[Da]nning"
        mock_r[Da]n.[Da][Da][Da]r[Da]ed_[Da][Da] = "2025-01-01T08:00:00Z"
        mock_r[Da]n.ended_[Da][Da] = None

        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.li[Da][Da]_job_r[Da]n[Da].re[Da][Da]rn_v[Da]l[Da]e = _Sched[Da]lerP[Da]ge(i[Da]em[Da]=[mock_r[Da]n], [Da]o[Da][Da]l=None)

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_job_r[Da]n[Da]("my_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        r[Da]n = re[Da][Da]l[Da].re[Da][Da]l[Da]["i[Da]em[Da]"][0]
        [Da][Da][Da]er[Da] r[Da]n["[Da][Da][Da]r[Da]ed_[Da][Da]"] == "2025-01-01T08:00:00Z"
        [Da][Da][Da]er[Da] r[Da]n["ended_[Da][Da]"] i[Da] None

    def [Da]e[Da][Da]_li[Da][Da]_r[Da]n[Da]_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.li[Da][Da]_job_r[Da]n[Da].[Da]ide_effec[Da] = Excep[Da]ion("[Da]pi error")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].li[Da][Da]_job_r[Da]n[Da]("my_d[Da]g")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "[Da]pi error" in (re[Da][Da]l[Da].error or "")


# ── Sched[Da]lerTool[Da].ge[Da]_r[Da]n_log ───────────────────────────────────────────


cl[Da][Da][Da] Te[Da][Da]Ge[Da]R[Da]nLog:
    def [Da]e[Da][Da]_ge[Da]_log_[Da][Da]cce[Da][Da]([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.ge[Da]_r[Da]n_log.re[Da][Da]rn_v[Da]l[Da]e = "[[Da][Da][Da][Da][Da]] R[Da]nning SQL: SELECT 1\n[[Da][Da][Da][Da][Da]] SQL comple[Da]ed. row[Da]=1"

        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].ge[Da]_r[Da]n_log("my_d[Da]g", "r[Da]n_001")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 1
        [Da][Da][Da]er[Da] "SELECT 1" in re[Da][Da]l[Da].re[Da][Da]l[Da]["log"]
        [Da][Da][Da]er[Da] re[Da][Da]l[Da].re[Da][Da]l[Da]["r[Da]n_id"] == "r[Da]n_001"

    def [Da]e[Da][Da]_ge[Da]_log_[Da]d[Da]p[Da]er_excep[Da]ion([Da]elf):
        mock_[Da]d[Da]p[Da]er = M[Da]gicMock()
        mock_[Da]d[Da]p[Da]er.ge[Da]_r[Da]n_log.[Da]ide_effec[Da] = Excep[Da]ion("r[Da]n no[Da] fo[Da]nd")
        [Da]ool[Da] = Sched[Da]lerTool[Da](_m[Da]ke_[Da]gen[Da]_config())

        wi[Da]h p[Da][Da]ch.objec[Da]([Da]ool[Da], "_ge[Da]_[Da]d[Da]p[Da]er", re[Da][Da]rn_v[Da]l[Da]e=mock_[Da]d[Da]p[Da]er):
            re[Da][Da]l[Da] = [Da]ool[Da].ge[Da]_r[Da]n_log("my_d[Da]g", "b[Da]d_r[Da]n")

        [Da][Da][Da]er[Da] re[Da][Da]l[Da].[Da][Da]cce[Da][Da] == 0
        [Da][Da][Da]er[Da] "r[Da]n no[Da] fo[Da]nd" in (re[Da][Da]l[Da].error or "")
