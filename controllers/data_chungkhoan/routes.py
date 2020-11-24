from flask import session, redirect, url_for, render_template, request

from jinja2 import TemplateNotFound
import config
import os, time, cv2
from flask_restplus import Api, Resource, Namespace
from flask import send_file
import numpy as np

from . import mod, namespace
from flask import Response

from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from app import es


def save_xls(list_dfs, xls_path, _list_indexs):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer, '%s' % str(_list_indexs[n])[:30])
        writer.save()


@namespace.route('/chungkhoan', methods=['GET', 'POST'])
class Download_data(Resource):
    def get(self):
        list_companys = ["AAA", "ABI", "ABS", "ACB", "ACV", "ADG", "AGG", "AGR", "AMD", "ANV", "ASM", "AST", "BCC",
                         "BCG", "BCM", "BFC", "BHN", "BIC", "BID", "BMI", "BMP", "BOT", "BSA", "BSI", "BSR", "BVH",
                         "BVS", "BWE", "C4G", "CAV", "CC1", "CEE", "CEO", "CHP", "CII", "CLC", "CLL", "CMG", "CNG",
                         "CRE", "CSC", "CSM", "CSV", "CTD", "CTF", "CTG", "CTI", "CTR", "CTS", "CVT", "D2D", "DBC",
                         "DBD", "DCL", "DCM", "DDV", "DGC", "DGW", "DHA", "DHC", "DHG", "DHT", "DIG", "DMC", "DNA",
                         "DNP", "DPG", "DPM", "DPR", "DQC", "DRC", "DRL", "DSN", "DSP", "DVN", "DVP", "DXG", "EIB",
                         "EVF", "FCN", "FIR", "FIT", "FLC", "FMC", "FOX", "FPT", "FTS", "GAB", "GAS", "GEG", "GEX",
                         "GMD", "GTN", "GVR", "HAG", "HAH", "HAI", "HBC", "HCM", "HDB", "HDC", "HDG", "HHC", "HHS",
                         "HNG", "HPG", "HPI", "HPX", "HQC", "HRC", "HSG", "HT1", "HTM", "HTN", "HVG", "HVN", "IBC",
                         "IDC", "IDI", "IDJ", "IDV", "IJC", "IMP", "ITA", "ITC", "KBC", "KDC", "KDF", "KDH", "KOS",
                         "KSB", "L14", "LAS", "LCG", "LDG", "LGC", "LHG", "LIX", "LPB", "LTG", "MBB", "MBS", "MCH",
                         "MEG", "MIG", "MML", "MPC", "MSH", "MSN", "MSR", "MWG", "NAF", "NBB", "NCT", "ND2", "NDN",
                         "NET", "NKG", "NLG", "NNC", "NT2", "NTC", "NTL", "NTP", "NVB", "NVL", "NVT", "OGC", "OIL",
                         "PAC", "PAN", "PC1", "PDN", "PDR", "PET", "PGC", "PGD", "PGI", "PGS", "PHP", "PHR", "PLC",
                         "PLX", "PME", "PMG", "PNJ", "POM", "POW", "PPC", "PTB", "PTI", "PVD", "PVI", "PVP", "PVS",
                         "PVT", "PXL", "QCG", "QNS", "RAL", "REE", "ROS", "SAB", "SAM", "SAS", "SBA", "SBM", "SBT",
                         "SCR", "SCS", "SDI", "SEA", "SGN", "SGP", "SGR", "SHB", "SHI", "SHN", "SHS", "SIP", "SJD",
                         "SJS", "SKG", "SKV", "SLS", "SMB", "SMC", "SNZ", "SRC", "SSI", "STB", "STG", "STK", "SVC",
                         "SVG", "SVI", "SWC", "SZB", "SZC", "SZL", "TAC", "TAR", "TBD", "TCB", "TCH", "TCM", "TDC",
                         "TDH", "TDM", "TDP", "THG", "THI", "TIG", "TIS", "TIX", "TLG", "TMG", "TMP", "TNA", "TNG",
                         "TNI", "TPB", "TRA", "TRC", "TV2", "TVB", "TVC", "TVN", "TVS", "VBB", "VC3", "VCB", "VCF",
                         "VCG", "VCI", "VCP", "VCS", "VCW", "VDS", "VEA", "VEF", "VGC", "VGG", "VGI", "VGR", "VGT",
                         "VHC", "VHM", "VIB", "VIC", "VIF", "VIS", "VIX", "VJC", "VLB", "VLC", "VNB", "VND", "VNG",
                         "VNM", "VNS", "VOC", "VPB", "VPD", "VPG", "VPI", "VRE", "VSC", "VSH", "VTO", "VTP", "VTR",
                         "WSB", "XHC", "YEG"]
        list_ids = list_companys[0:20]
        list_indexs = ["_cophieu68_loi_nhuan_eps_pe", "_stock_gd_co_dong_chinh", "_stock_biz_gia_qua_khu",
                       "_stock_biz_giao_dich_ndtnn", "_stock_biz_thong_ke_dat_lenh", "_tong_hop"]
        return Response(render_template('index_chungkhoan.html', list_ids=list_ids, list_indexs=list_indexs), 200,
                        mimetype='text/html')

    def post(self):
        # check if the post request has the file part
        if not request.form:
            abort(400)
        print(request.form)
        ma = request.form.get('ma').lower()
        from_date = request.form.get('from') or '01/01/2014'
        to_date = request.form.get('to') or '01/01/2050'
        from_date = from_date.split('/')[2] + '-' + from_date.split('/')[0] + '-' + from_date.split('/')[1]
        to_date = to_date.split('/')[2] + '-' + to_date.split('/')[0] + '-' + to_date.split('/')[1]
        list_indexs = ["_cophieu68_loi_nhuan_eps_pe", "_stock_gd_co_dong_chinh", "_stock_biz_gia_qua_khu",
                       "_stock_biz_giao_dich_ndtnn", "_stock_biz_thong_ke_dat_lenh", "_tong_hop"]
        _list_indexs = []
        for index in list_indexs:
            if request.form.get(index):
                _list_indexs.append(index)
        list_data_frames = []
        for index in _list_indexs:

            result = es.search(index=ma + index, body={
                "query": {
                    "range": {  # expect this to return the one result on 2012-12-20
                        "date_time": {
                            "gte": from_date,
                            "lte": to_date,
                        }
                    }
                }}, size=2000)
            elastic_docs = result["hits"]["hits"]

            fields = {}

            for num, doc in enumerate(elastic_docs):
                _id = doc["_id"]

                # get source data from document
                source_data = doc["_source"]
                for key, val in source_data.items():
                    try:
                        fields[key] = np.append(fields[key], val)
                    except KeyError:
                        fields[key] = np.array([val])

            elastic_df = pd.DataFrame(fields)
            elastic_df.sort_values(by=['date_time'], inplace=True, ascending=False)
            elastic_df.set_index(['date_time'], inplace=True)
            list_data_frames.append(elastic_df)
        save_xls(list_data_frames, 'static/data_' + ma + from_date + '_to_' + to_date + '.xlsx', _list_indexs)
        return send_file('static/data_' + ma + from_date + '_to_' + to_date + '.xlsx',
                         as_attachment=True, cache_timeout=0)
