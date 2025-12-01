# 한국투자증권(KIS) 국내주식 및 ETF 관련 REST API 7종에 대한 OpenAPI 3.0 Specification(JSON 포맷)

> ## 마지막에 연동 시 참고할 가이드라인을 첨부했습니다

---

### 1. ETF/ETN 현재가 [v1_국내주식-068]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "ETF/ETN 현재가",
    "version": "v1_domestic_stock_068",
    "description": "ETF/ETN 종목의 현재가 및 상세 정보를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    }
  ],
  "paths": {
    "/uapi/etfetn/v1/quotations/inquire-price": {
      "get": {
        "summary": "ETF/ETN 현재가 조회",
        "operationId": "inquireEtfEtnPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHPST02400000)",
            "schema": { "type": "string", "example": "FHPST02400000" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "fid_input_iscd",
            "in": "query",
            "required": true,
            "description": "FID 입력 종목코드",
            "schema": { "type": "string" }
          },
          {
            "name": "fid_cond_mrkt_div_code",
            "in": "query",
            "required": true,
            "description": "FID 조건 시장 분류 코드 (J)",
            "schema": { "type": "string", "example": "J" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output": {
                      "type": "object",
                      "properties": {
                        "stck_prpr": { "type": "string" },
                        "prdy_vrss_sign": { "type": "string" },
                        "prdy_vrss": { "type": "string" },
                        "prdy_ctrt": { "type": "string" },
                        "acml_vol": { "type": "string" },
                        "prdy_vol": { "type": "string" },
                        "stck_mxpr": { "type": "string" },
                        "stck_llam": { "type": "string" },
                        "stck_prdy_clpr": { "type": "string" },
                        "stck_oprc": { "type": "string" },
                        "prdy_clpr_vrss_oprc_rate": { "type": "string" },
                        "stck_hgpr": { "type": "string" },
                        "prdy_clpr_vrss_hgpr_rate": { "type": "string" },
                        "stck_lwpr": { "type": "string" },
                        "prdy_clpr_vrss_lwpr_rate": { "type": "string" },
                        "prdy_last_nav": { "type": "string" },
                        "nav": { "type": "string" },
                        "nav_prdy_vrss": { "type": "string" },
                        "nav_prdy_vrss_sign": { "type": "string" },
                        "nav_prdy_ctrt": { "type": "string" },
                        "trc_errt": { "type": "string" },
                        "stck_sdpr": { "type": "string" },
                        "stck_sspr": { "type": "string" },
                        "nmix_ctrt": { "type": "string" },
                        "etf_crcl_stcn": { "type": "string" },
                        "etf_ntas_ttam": { "type": "string" },
                        "etf_frcr_ntas_ttam": { "type": "string" },
                        "frgn_limt_rate": { "type": "string" },
                        "frgn_oder_able_qty": { "type": "string" },
                        "etf_cu_unit_scrt_cnt": { "type": "string" },
                        "etf_cnfg_issu_cnt": { "type": "string" },
                        "etf_dvdn_cycl": { "type": "string" },
                        "crcd": { "type": "string" },
                        "etf_crcl_ntas_ttam": { "type": "string" },
                        "etf_frcr_crcl_ntas_ttam": { "type": "string" },
                        "etf_frcr_last_ntas_wrth_val": { "type": "string" },
                        "lp_oder_able_cls_code": { "type": "string" },
                        "stck_dryy_hgpr": { "type": "string" },
                        "dryy_hgpr_vrss_prpr_rate": { "type": "string" },
                        "dryy_hgpr_date": { "type": "string" },
                        "stck_dryy_lwpr": { "type": "string" },
                        "dryy_lwpr_vrss_prpr_rate": { "type": "string" },
                        "dryy_lwpr_date": { "type": "string" },
                        "bstp_kor_isnm": { "type": "string" },
                        "vi_cls_code": { "type": "string" },
                        "lstn_stcn": { "type": "string" },
                        "frgn_hldn_qty": { "type": "string" },
                        "frgn_hldn_qty_rate": { "type": "string" },
                        "etf_trc_ert_mltp": { "type": "string" },
                        "dprt": { "type": "string" },
                        "mbcr_name": { "type": "string" },
                        "stck_lstn_date": { "type": "string" },
                        "mtrt_date": { "type": "string" },
                        "shrg_type_code": { "type": "string" },
                        "lp_hldn_rate": { "type": "string" },
                        "etf_trgt_nmix_bstp_code": { "type": "string" },
                        "etf_div_name": { "type": "string" },
                        "etf_rprs_bstp_kor_isnm": { "type": "string" },
                        "lp_hldn_vol": { "type": "string" }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 2. ETF 구성종목시세 [국내주식-073]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "ETF 구성종목시세",
    "version": "v1_domestic_stock_073",
    "description": "ETF의 구성종목 및 해당 종목의 시세를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    }
  ],
  "paths": {
    "/uapi/etfetn/v1/quotations/inquire-component-stock-price": {
      "get": {
        "summary": "ETF 구성종목시세 조회",
        "operationId": "inquireComponentStockPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHKST121600C0)",
            "schema": { "type": "string", "example": "FHKST121600C0" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "FID_COND_MRKT_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건시장분류코드 (J)",
            "schema": { "type": "string", "example": "J" }
          },
          {
            "name": "FID_INPUT_ISCD",
            "in": "query",
            "required": true,
            "description": "입력종목코드",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_COND_SCR_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건화면분류코드 (11216)",
            "schema": { "type": "string", "example": "11216" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output1": {
                      "type": "object",
                      "properties": {
                        "stck_prpr": { "type": "string" },
                        "prdy_vrss": { "type": "string" },
                        "prdy_vrss_sign": { "type": "string" },
                        "prdy_ctrt": { "type": "string" },
                        "etf_cnfg_issu_avls": { "type": "string" },
                        "nav": { "type": "string" },
                        "nav_prdy_vrss_sign": { "type": "string" },
                        "nav_prdy_vrss": { "type": "string" },
                        "nav_prdy_ctrt": { "type": "string" },
                        "etf_ntas_ttam": { "type": "string" },
                        "prdy_clpr_nav": { "type": "string" },
                        "oprc_nav": { "type": "string" },
                        "hprc_nav": { "type": "string" },
                        "lprc_nav": { "type": "string" },
                        "etf_cu_unit_scrt_cnt": { "type": "string" },
                        "etf_cnfg_issu_cnt": { "type": "string" }
                      }
                    },
                    "output2": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "stck_shrn_iscd": { "type": "string" },
                          "hts_kor_isnm": { "type": "string" },
                          "stck_prpr": { "type": "string" },
                          "prdy_vrss": { "type": "string" },
                          "prdy_vrss_sign": { "type": "string" },
                          "prdy_ctrt": { "type": "string" },
                          "acml_vol": { "type": "string" },
                          "acml_tr_pbmn": { "type": "string" },
                          "tday_rsfl_rate": { "type": "string" },
                          "prdy_vrss_vol": { "type": "string" },
                          "tr_pbmn_tnrt": { "type": "string" },
                          "hts_avls": { "type": "string" },
                          "etf_cnfg_issu_avls": { "type": "string" },
                          "etf_cnfg_issu_rlim": { "type": "string" },
                          "etf_vltn_amt": { "type": "string" }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 3. 국내주식기간별시세(일/주/월/년) [v1_국내주식-016]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "국내주식기간별시세(일/주/월/년)",
    "version": "v1_domestic_stock_016",
    "description": "국내주식 종목의 기간별 시세(일/주/월/년)를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    },
    {
      "url": "https://openapivts.koreainvestment.com:29443",
      "description": "모의 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice": {
      "get": {
        "summary": "국내주식기간별시세 조회",
        "operationId": "inquireDailyItemChartPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHKST03010100)",
            "schema": { "type": "string", "example": "FHKST03010100" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입 (P:개인, B:법인)",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "FID_COND_MRKT_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건 시장 분류 코드 (J:KRX, NX:NXT, UN:통합)",
            "schema": { "type": "string", "example": "J" }
          },
          {
            "name": "FID_INPUT_ISCD",
            "in": "query",
            "required": true,
            "description": "입력 종목코드 (ex: 005930)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_INPUT_DATE_1",
            "in": "query",
            "required": true,
            "description": "조회 시작일자 (YYYYMMDD)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_INPUT_DATE_2",
            "in": "query",
            "required": true,
            "description": "조회 종료일자 (YYYYMMDD)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_PERIOD_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "기간분류코드 (D:일봉, W:주봉, M:월봉, Y:년봉)",
            "schema": { "type": "string", "example": "D" }
          },
          {
            "name": "FID_ORG_ADJ_PRC",
            "in": "query",
            "required": true,
            "description": "수정주가/원주가 여부 (0:수정주가, 1:원주가)",
            "schema": { "type": "string", "example": "0" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": {
                      "type": "string",
                      "description": "성공 실패 여부"
                    },
                    "msg_cd": { "type": "string", "description": "응답코드" },
                    "msg1": { "type": "string", "description": "응답메세지" },
                    "output1": {
                      "type": "object",
                      "properties": {
                        "prdy_vrss": { "type": "string" },
                        "prdy_vrss_sign": { "type": "string" },
                        "prdy_ctrt": { "type": "string" },
                        "stck_prdy_clpr": { "type": "string" },
                        "acml_vol": { "type": "string" },
                        "acml_tr_pbmn": { "type": "string" },
                        "hts_kor_isnm": { "type": "string" },
                        "stck_prpr": { "type": "string" },
                        "stck_shrn_iscd": { "type": "string" },
                        "prdy_vol": { "type": "string" },
                        "stck_mxpr": { "type": "string" },
                        "stck_llam": { "type": "string" },
                        "stck_oprc": { "type": "string" },
                        "stck_hgpr": { "type": "string" },
                        "stck_lwpr": { "type": "string" },
                        "stck_prdy_oprc": { "type": "string" },
                        "stck_prdy_hgpr": { "type": "string" },
                        "stck_prdy_lwpr": { "type": "string" },
                        "askp": { "type": "string" },
                        "bidp": { "type": "string" },
                        "prdy_vrss_vol": { "type": "string" },
                        "vol_tnrt": { "type": "string" },
                        "stck_fcam": { "type": "string" },
                        "lstn_stcn": { "type": "string" },
                        "cpfn": { "type": "string" },
                        "hts_avls": { "type": "string" },
                        "per": { "type": "string" },
                        "eps": { "type": "string" },
                        "pbr": { "type": "string" },
                        "itewhol_loan_rmnd_ratem": { "type": "string" }
                      }
                    },
                    "output2": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "stck_bsop_date": { "type": "string" },
                          "stck_clpr": { "type": "string" },
                          "stck_oprc": { "type": "string" },
                          "stck_hgpr": { "type": "string" },
                          "stck_lwpr": { "type": "string" },
                          "acml_vol": { "type": "string" },
                          "acml_tr_pbmn": { "type": "string" },
                          "flng_cls_code": { "type": "string" },
                          "prtt_rate": { "type": "string" },
                          "mod_yn": { "type": "string" },
                          "prdy_vrss_sign": { "type": "string" },
                          "prdy_vrss": { "type": "string" },
                          "revl_issu_reas": { "type": "string" }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 4. 주식기본조회 [v1_국내주식-067]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "주식기본조회",
    "version": "v1_domestic_stock_067",
    "description": "국내주식 종목의 종목상세정보를 확인하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/search-stock-info": {
      "get": {
        "summary": "주식기본조회",
        "operationId": "searchStockInfo",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (CTPF1002R)",
            "schema": { "type": "string", "example": "CTPF1002R" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "PRDT_TYPE_CD",
            "in": "query",
            "required": true,
            "description": "상품유형코드 (300:주식/ETF/ETN/ELW 등)",
            "schema": { "type": "string", "example": "300" }
          },
          {
            "name": "PDNO",
            "in": "query",
            "required": true,
            "description": "상품번호 (종목번호 6자리)",
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output": {
                      "type": "object",
                      "properties": {
                        "pdno": { "type": "string" },
                        "prdt_type_cd": { "type": "string" },
                        "mket_id_cd": { "type": "string" },
                        "scty_grp_id_cd": { "type": "string" },
                        "excg_dvsn_cd": { "type": "string" },
                        "setl_mmdd": { "type": "string" },
                        "lstg_stqt": { "type": "string" },
                        "lstg_cptl_amt": { "type": "string" },
                        "cpta": { "type": "string" },
                        "papr": { "type": "string" },
                        "issu_pric": { "type": "string" },
                        "kospi200_item_yn": { "type": "string" },
                        "scts_mket_lstg_dt": { "type": "string" },
                        "scts_mket_lstg_abol_dt": { "type": "string" },
                        "kosdaq_mket_lstg_dt": { "type": "string" },
                        "kosdaq_mket_lstg_abol_dt": { "type": "string" },
                        "frbd_mket_lstg_dt": { "type": "string" },
                        "frbd_mket_lstg_abol_dt": { "type": "string" },
                        "reits_kind_cd": { "type": "string" },
                        "etf_dvsn_cd": { "type": "string" },
                        "oilf_fund_yn": { "type": "string" },
                        "idx_bztp_lcls_cd": { "type": "string" },
                        "idx_bztp_mcls_cd": { "type": "string" },
                        "idx_bztp_scls_cd": { "type": "string" },
                        "stck_kind_cd": { "type": "string" },
                        "mfnd_opng_dt": { "type": "string" },
                        "mfnd_end_dt": { "type": "string" },
                        "dpsi_erlm_cncl_dt": { "type": "string" },
                        "etf_cu_qty": { "type": "string" },
                        "prdt_name": { "type": "string" },
                        "prdt_name120": { "type": "string" },
                        "prdt_abrv_name": { "type": "string" },
                        "std_pdno": { "type": "string" },
                        "prdt_eng_name": { "type": "string" },
                        "prdt_eng_name120": { "type": "string" },
                        "prdt_eng_abrv_name": { "type": "string" },
                        "dpsi_aptm_erlm_yn": { "type": "string" },
                        "etf_txtn_type_cd": { "type": "string" },
                        "etf_type_cd": { "type": "string" },
                        "lstg_abol_dt": { "type": "string" },
                        "nwst_odst_dvsn_cd": { "type": "string" },
                        "sbst_pric": { "type": "string" },
                        "thco_sbst_pric": { "type": "string" },
                        "thco_sbst_pric_chng_dt": { "type": "string" },
                        "tr_stop_yn": { "type": "string" },
                        "admn_item_yn": { "type": "string" },
                        "thdt_clpr": { "type": "string" },
                        "bfdy_clpr": { "type": "string" },
                        "clpr_chng_dt": { "type": "string" },
                        "std_idst_clsf_cd": { "type": "string" },
                        "std_idst_clsf_cd_name": { "type": "string" },
                        "idx_bztp_lcls_cd_name": { "type": "string" },
                        "idx_bztp_mcls_cd_name": { "type": "string" },
                        "idx_bztp_scls_cd_name": { "type": "string" },
                        "ocr_no": { "type": "string" },
                        "crfd_item_yn": { "type": "string" },
                        "elec_scty_yn": { "type": "string" },
                        "issu_istt_cd": { "type": "string" },
                        "etf_chas_erng_rt_dbnb": { "type": "string" },
                        "etf_etn_ivst_heed_item_yn": { "type": "string" },
                        "stln_int_rt_dvsn_cd": { "type": "string" },
                        "frnr_psnl_lmt_rt": { "type": "string" },
                        "lstg_rqsr_issu_istt_cd": { "type": "string" },
                        "lstg_rqsr_item_cd": { "type": "string" },
                        "trst_istt_issu_istt_cd": { "type": "string" },
                        "cptt_trad_tr_psbl_yn": { "type": "string" },
                        "nxt_tr_stop_yn": { "type": "string" }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 5. 상품기본조회 [v1_국내주식-029]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "상품기본조회",
    "version": "v1_domestic_stock_029",
    "description": "주식, 선물옵션, 해외주식 등의 상품 기본 정보를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/search-info": {
      "get": {
        "summary": "상품기본조회",
        "operationId": "searchProductInfo",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (CTPF1604R)",
            "schema": { "type": "string", "example": "CTPF1604R" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입 (P:개인, B:법인)",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "PDNO",
            "in": "query",
            "required": true,
            "description": "상품번호 (예: 000660)",
            "schema": { "type": "string" }
          },
          {
            "name": "PRDT_TYPE_CD",
            "in": "query",
            "required": true,
            "description": "상품유형코드 (300:주식, 301:선물옵션 등)",
            "schema": { "type": "string", "example": "300" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": {
                      "type": "string",
                      "description": "성공 실패 여부"
                    },
                    "msg_cd": { "type": "string", "description": "응답코드" },
                    "msg1": { "type": "string", "description": "응답메세지" },
                    "output": {
                      "type": "object",
                      "description": "응답상세",
                      "properties": {
                        "pdno": { "type": "string", "description": "상품번호" },
                        "prdt_type_cd": {
                          "type": "string",
                          "description": "상품유형코드"
                        },
                        "prdt_name": {
                          "type": "string",
                          "description": "상품명"
                        },
                        "prdt_name120": {
                          "type": "string",
                          "description": "상품명120"
                        },
                        "prdt_abrv_name": {
                          "type": "string",
                          "description": "상품약어명"
                        },
                        "prdt_eng_name": {
                          "type": "string",
                          "description": "상품영문명"
                        },
                        "prdt_eng_name120": {
                          "type": "string",
                          "description": "상품영문명120"
                        },
                        "prdt_eng_abrv_name": {
                          "type": "string",
                          "description": "상품영문약어명"
                        },
                        "std_pdno": {
                          "type": "string",
                          "description": "표준상품번호"
                        },
                        "shtn_pdno": {
                          "type": "string",
                          "description": "단축상품번호"
                        },
                        "prdt_sale_stat_cd": {
                          "type": "string",
                          "description": "상품판매상태코드"
                        },
                        "prdt_risk_grad_cd": {
                          "type": "string",
                          "description": "상품위험등급코드"
                        },
                        "prdt_clsf_cd": {
                          "type": "string",
                          "description": "상품분류코드"
                        },
                        "prdt_clsf_name": {
                          "type": "string",
                          "description": "상품분류명"
                        },
                        "sale_strt_dt": {
                          "type": "string",
                          "description": "판매시작일자"
                        },
                        "sale_end_dt": {
                          "type": "string",
                          "description": "판매종료일자"
                        },
                        "wrap_asst_type_cd": {
                          "type": "string",
                          "description": "랩어카운트자산유형코드"
                        },
                        "ivst_prdt_type_cd": {
                          "type": "string",
                          "description": "투자상품유형코드"
                        },
                        "ivst_prdt_type_cd_name": {
                          "type": "string",
                          "description": "투자상품유형코드명"
                        },
                        "frst_erlm_dt": {
                          "type": "string",
                          "description": "최초등록일자"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 6. 국내주식업종기간별시세(일/주/월/년) [v1_국내주식-021]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "국내주식 업종기간별시세",
    "version": "v1_domestic_stock_021",
    "description": "국내주식 업종의 일/주/월/년 단위 시세를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    },
    {
      "url": "https://openapivts.koreainvestment.com:29443",
      "description": "모의 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/inquire-daily-indexchartprice": {
      "get": {
        "summary": "업종기간별시세 조회",
        "operationId": "inquireDailyIndexChartPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHKUP03500100)",
            "schema": { "type": "string", "example": "FHKUP03500100" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "FID_COND_MRKT_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건 시장 분류 코드 (업종: U)",
            "schema": { "type": "string", "example": "U" }
          },
          {
            "name": "FID_INPUT_ISCD",
            "in": "query",
            "required": true,
            "description": "업종 상세코드 (0001: 종합 등)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_INPUT_DATE_1",
            "in": "query",
            "required": true,
            "description": "조회 시작일자 (YYYYMMDD)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_INPUT_DATE_2",
            "in": "query",
            "required": true,
            "description": "조회 종료일자 (YYYYMMDD)",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_PERIOD_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "기간분류코드 (D:일봉, W:주봉, M:월봉, Y:년봉)",
            "schema": { "type": "string", "example": "D" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output1": {
                      "type": "object",
                      "description": "응답상세 (현재 상태)",
                      "properties": {
                        "prdy_vrss_sign": {
                          "type": "string",
                          "description": "전일 대비 부호"
                        },
                        "bstp_nmix_prdy_ctrt": {
                          "type": "string",
                          "description": "업종 지수 전일 대비율"
                        },
                        "prdy_nmix": {
                          "type": "string",
                          "description": "전일 지수"
                        },
                        "acml_vol": {
                          "type": "string",
                          "description": "누적 거래량"
                        },
                        "acml_tr_pbmn": {
                          "type": "string",
                          "description": "누적 거래 대금"
                        },
                        "hts_kor_isnm": {
                          "type": "string",
                          "description": "HTS 한글 종목명"
                        },
                        "bstp_nmix_prpr": {
                          "type": "string",
                          "description": "업종 지수 현재가"
                        },
                        "bstp_cls_code": {
                          "type": "string",
                          "description": "업종 구분 코드"
                        },
                        "prdy_vol": {
                          "type": "string",
                          "description": "전일 거래량"
                        },
                        "bstp_nmix_oprc": {
                          "type": "string",
                          "description": "업종 지수 시가2"
                        },
                        "bstp_nmix_hgpr": {
                          "type": "string",
                          "description": "업종 지수 최고가"
                        },
                        "bstp_nmix_lwpr": {
                          "type": "string",
                          "description": "업종 지수 최저가"
                        },
                        "futs_prdy_oprc": {
                          "type": "string",
                          "description": "선물 전일 시가"
                        },
                        "futs_prdy_hgpr": {
                          "type": "string",
                          "description": "선물 전일 최고가"
                        },
                        "futs_prdy_lwpr": {
                          "type": "string",
                          "description": "선물 전일 최저가"
                        }
                      }
                    },
                    "output2": {
                      "type": "array",
                      "description": "응답상세 (기간별 데이터)",
                      "items": {
                        "type": "object",
                        "properties": {
                          "stck_bsop_date": {
                            "type": "string",
                            "description": "주식 영업 일자"
                          },
                          "bstp_nmix_prpr": {
                            "type": "string",
                            "description": "업종 지수 현재가"
                          },
                          "bstp_nmix_oprc": {
                            "type": "string",
                            "description": "업종 지수 시가2"
                          },
                          "bstp_nmix_hgpr": {
                            "type": "string",
                            "description": "업종 지수 최고가"
                          },
                          "bstp_nmix_lwpr": {
                            "type": "string",
                            "description": "업종 지수 최저가"
                          },
                          "acml_vol": {
                            "type": "string",
                            "description": "누적 거래량"
                          },
                          "acml_tr_pbmn": {
                            "type": "string",
                            "description": "누적 거래 대금"
                          },
                          "mod_yn": {
                            "type": "string",
                            "description": "변경 여부"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 7. 주식현재가 시세 [v1_국내주식-008]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "주식현재가 시세",
    "version": "v1_domestic_stock_008",
    "description": "주식 종목의 현재가 및 상세 정보를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    },
    {
      "url": "https://openapivts.koreainvestment.com:29443",
      "description": "모의 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/inquire-price": {
      "get": {
        "summary": "주식 현재가 조회",
        "operationId": "inquireStockPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHKST01010100)",
            "schema": { "type": "string", "example": "FHKST01010100" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "FID_COND_MRKT_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건 시장 분류 코드 (J:KRX)",
            "schema": { "type": "string", "example": "J" }
          },
          {
            "name": "FID_INPUT_ISCD",
            "in": "query",
            "required": true,
            "description": "입력 종목코드",
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output": {
                      "type": "object",
                      "description": "응답상세",
                      "properties": {
                        "iscd_stat_cls_code": {
                          "type": "string",
                          "description": "종목 상태 구분 코드"
                        },
                        "marg_rate": {
                          "type": "string",
                          "description": "증거금 비율"
                        },
                        "rprs_mrkt_kor_name": {
                          "type": "string",
                          "description": "대표 시장 한글 명"
                        },
                        "new_hgpr_lwpr_cls_code": {
                          "type": "string",
                          "description": "신 고가 저가 구분 코드"
                        },
                        "bstp_kor_isnm": {
                          "type": "string",
                          "description": "업종 한글 종목명"
                        },
                        "temp_stop_yn": {
                          "type": "string",
                          "description": "임시 정지 여부"
                        },
                        "oprc_rang_cont_yn": {
                          "type": "string",
                          "description": "시가 범위 연장 여부"
                        },
                        "clpr_rang_cont_yn": {
                          "type": "string",
                          "description": "종가 범위 연장 여부"
                        },
                        "crdt_able_yn": {
                          "type": "string",
                          "description": "신용 가능 여부"
                        },
                        "grmn_rate_cls_code": {
                          "type": "string",
                          "description": "보증금 비율 구분 코드"
                        },
                        "elw_pblc_yn": {
                          "type": "string",
                          "description": "ELW 발행 여부"
                        },
                        "stck_prpr": {
                          "type": "string",
                          "description": "주식 현재가"
                        },
                        "prdy_vrss": {
                          "type": "string",
                          "description": "전일 대비"
                        },
                        "prdy_vrss_sign": {
                          "type": "string",
                          "description": "전일 대비 부호"
                        },
                        "prdy_ctrt": {
                          "type": "string",
                          "description": "전일 대비율"
                        },
                        "acml_tr_pbmn": {
                          "type": "string",
                          "description": "누적 거래 대금"
                        },
                        "acml_vol": {
                          "type": "string",
                          "description": "누적 거래량"
                        },
                        "prdy_vrss_vol_rate": {
                          "type": "string",
                          "description": "전일 대비 거래량 비율"
                        },
                        "stck_oprc": {
                          "type": "string",
                          "description": "주식 시가2"
                        },
                        "stck_hgpr": {
                          "type": "string",
                          "description": "주식 최고가"
                        },
                        "stck_lwpr": {
                          "type": "string",
                          "description": "주식 최저가"
                        },
                        "stck_mxpr": {
                          "type": "string",
                          "description": "주식 상한가"
                        },
                        "stck_llam": {
                          "type": "string",
                          "description": "주식 하한가"
                        },
                        "stck_sdpr": {
                          "type": "string",
                          "description": "주식 기준가"
                        },
                        "wghn_avrg_stck_prc": {
                          "type": "string",
                          "description": "가중 평균 주식 가격"
                        },
                        "hts_frgn_ehrt": {
                          "type": "string",
                          "description": "HTS 외국인 소진율"
                        },
                        "frgn_ntby_qty": {
                          "type": "string",
                          "description": "외국인 순매수 수량"
                        },
                        "pgtr_ntby_qty": {
                          "type": "string",
                          "description": "프로그램매매 순매수 수량"
                        },
                        "pvt_scnd_dmrs_prc": {
                          "type": "string",
                          "description": "피벗 2차 디저항 가격"
                        },
                        "pvt_frst_dmrs_prc": {
                          "type": "string",
                          "description": "피벗 1차 디저항 가격"
                        },
                        "pvt_pont_val": {
                          "type": "string",
                          "description": "피벗 포인트 값"
                        },
                        "pvt_frst_dmsp_prc": {
                          "type": "string",
                          "description": "피벗 1차 디지지 가격"
                        },
                        "pvt_scnd_dmsp_prc": {
                          "type": "string",
                          "description": "피벗 2차 디지지 가격"
                        },
                        "dmrs_val": {
                          "type": "string",
                          "description": "디저항 값"
                        },
                        "dmsp_val": {
                          "type": "string",
                          "description": "디지지 값"
                        },
                        "cpfn": { "type": "string", "description": "자본금" },
                        "rstc_wdth_prc": {
                          "type": "string",
                          "description": "제한 폭 가격"
                        },
                        "stck_fcam": {
                          "type": "string",
                          "description": "주식 액면가"
                        },
                        "stck_sspr": {
                          "type": "string",
                          "description": "주식 대용가"
                        },
                        "aspr_unit": {
                          "type": "string",
                          "description": "호가단위"
                        },
                        "hts_deal_qty_unit_val": {
                          "type": "string",
                          "description": "HTS 매매 수량 단위 값"
                        },
                        "lstn_stcn": {
                          "type": "string",
                          "description": "상장 주수"
                        },
                        "hts_avls": {
                          "type": "string",
                          "description": "HTS 시가총액"
                        },
                        "per": { "type": "string", "description": "PER" },
                        "pbr": { "type": "string", "description": "PBR" },
                        "stac_month": {
                          "type": "string",
                          "description": "결산 월"
                        },
                        "vol_tnrt": {
                          "type": "string",
                          "description": "거래량 회전율"
                        },
                        "eps": { "type": "string", "description": "EPS" },
                        "bps": { "type": "string", "description": "BPS" },
                        "d250_hgpr": {
                          "type": "string",
                          "description": "250일 최고가"
                        },
                        "d250_hgpr_date": {
                          "type": "string",
                          "description": "250일 최고가 일자"
                        },
                        "d250_hgpr_vrss_prpr_rate": {
                          "type": "string",
                          "description": "250일 최고가 대비 현재가 비율"
                        },
                        "d250_lwpr": {
                          "type": "string",
                          "description": "250일 최저가"
                        },
                        "d250_lwpr_date": {
                          "type": "string",
                          "description": "250일 최저가 일자"
                        },
                        "d250_lwpr_vrss_prpr_rate": {
                          "type": "string",
                          "description": "250일 최저가 대비 현재가 비율"
                        },
                        "stck_dryy_hgpr": {
                          "type": "string",
                          "description": "주식 연중 최고가"
                        },
                        "dryy_hgpr_vrss_prpr_rate": {
                          "type": "string",
                          "description": "연중 최고가 대비 현재가 비율"
                        },
                        "dryy_hgpr_date": {
                          "type": "string",
                          "description": "연중 최고가 일자"
                        },
                        "stck_dryy_lwpr": {
                          "type": "string",
                          "description": "주식 연중 최저가"
                        },
                        "dryy_lwpr_vrss_prpr_rate": {
                          "type": "string",
                          "description": "연중 최저가 대비 현재가 비율"
                        },
                        "dryy_lwpr_date": {
                          "type": "string",
                          "description": "연중 최저가 일자"
                        },
                        "w52_hgpr": {
                          "type": "string",
                          "description": "52주일 최고가"
                        },
                        "w52_hgpr_vrss_prpr_ctrt": {
                          "type": "string",
                          "description": "52주일 최고가 대비 현재가 대비"
                        },
                        "w52_hgpr_date": {
                          "type": "string",
                          "description": "52주일 최고가 일자"
                        },
                        "w52_lwpr": {
                          "type": "string",
                          "description": "52주일 최저가"
                        },
                        "w52_lwpr_vrss_prpr_ctrt": {
                          "type": "string",
                          "description": "52주일 최저가 대비 현재가 대비"
                        },
                        "w52_lwpr_date": {
                          "type": "string",
                          "description": "52주일 최저가 일자"
                        },
                        "whol_loan_rmnd_rate": {
                          "type": "string",
                          "description": "전체 융자 잔고 비율"
                        },
                        "ssts_yn": {
                          "type": "string",
                          "description": "공매도가능여부"
                        },
                        "stck_shrn_iscd": {
                          "type": "string",
                          "description": "주식 단축 종목코드"
                        },
                        "fcam_cnnm": {
                          "type": "string",
                          "description": "액면가 통화명"
                        },
                        "cpfn_cnnm": {
                          "type": "string",
                          "description": "자본금 통화명"
                        },
                        "apprch_rate": {
                          "type": "string",
                          "description": "접근도"
                        },
                        "frgn_hldn_qty": {
                          "type": "string",
                          "description": "외국인 보유 수량"
                        },
                        "vi_cls_code": {
                          "type": "string",
                          "description": "VI적용구분코드"
                        },
                        "ovtm_vi_cls_code": {
                          "type": "string",
                          "description": "시간외단일가VI적용구분코드"
                        },
                        "last_ssts_cntg_qty": {
                          "type": "string",
                          "description": "최종 공매도 체결 수량"
                        },
                        "invt_caful_yn": {
                          "type": "string",
                          "description": "투자유의여부"
                        },
                        "mrkt_warn_cls_code": {
                          "type": "string",
                          "description": "시장경고코드"
                        },
                        "short_over_yn": {
                          "type": "string",
                          "description": "단기과열여부"
                        },
                        "sltr_yn": {
                          "type": "string",
                          "description": "정리매매여부"
                        },
                        "mang_issu_cls_code": {
                          "type": "string",
                          "description": "관리종목여부"
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 8. 주식현재가 일자별 [v1_국내주식-010]

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "주식현재가 일자별",
    "version": "v1_domestic_stock_010",
    "description": "주식의 일/주/월별 시세 데이터를 조회하는 API입니다."
  },
  "servers": [
    {
      "url": "https://openapi.koreainvestment.com:9443",
      "description": "실전 Domain"
    },
    {
      "url": "https://openapivts.koreainvestment.com:29443",
      "description": "모의 Domain"
    }
  ],
  "paths": {
    "/uapi/domestic-stock/v1/quotations/inquire-daily-price": {
      "get": {
        "summary": "주식 일자별 시세 조회",
        "operationId": "inquireDailyStockPrice",
        "parameters": [
          {
            "name": "content-type",
            "in": "header",
            "required": true,
            "schema": {
              "type": "string",
              "example": "application/json; charset=utf-8"
            }
          },
          {
            "name": "authorization",
            "in": "header",
            "required": true,
            "description": "OAuth 접근 토큰",
            "schema": { "type": "string" }
          },
          {
            "name": "appkey",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppKey",
            "schema": { "type": "string" }
          },
          {
            "name": "appsecret",
            "in": "header",
            "required": true,
            "description": "한국투자증권 발급 AppSecret",
            "schema": { "type": "string" }
          },
          {
            "name": "tr_id",
            "in": "header",
            "required": true,
            "description": "거래ID (FHKST01010400)",
            "schema": { "type": "string", "example": "FHKST01010400" }
          },
          {
            "name": "custtype",
            "in": "header",
            "required": true,
            "description": "고객 타입",
            "schema": { "type": "string", "example": "P" }
          },
          {
            "name": "FID_COND_MRKT_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "조건 시장 분류 코드 (J:KRX)",
            "schema": { "type": "string", "example": "J" }
          },
          {
            "name": "FID_INPUT_ISCD",
            "in": "query",
            "required": true,
            "description": "입력 종목코드",
            "schema": { "type": "string" }
          },
          {
            "name": "FID_PERIOD_DIV_CODE",
            "in": "query",
            "required": true,
            "description": "기간 분류 코드 (D:일, W:주, M:월)",
            "schema": { "type": "string", "example": "D" }
          },
          {
            "name": "FID_ORG_ADJ_PRC",
            "in": "query",
            "required": true,
            "description": "수정주가 원주가 가격 (0:미반영, 1:반영)",
            "schema": { "type": "string", "example": "0" }
          }
        ],
        "responses": {
          "200": {
            "description": "성공",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "rt_cd": { "type": "string" },
                    "msg_cd": { "type": "string" },
                    "msg1": { "type": "string" },
                    "output": {
                      "type": "array",
                      "description": "응답상세 (일자별 데이터)",
                      "items": {
                        "type": "object",
                        "properties": {
                          "stck_bsop_date": {
                            "type": "string",
                            "description": "주식 영업 일자"
                          },
                          "stck_oprc": {
                            "type": "string",
                            "description": "주식 시가2"
                          },
                          "stck_hgpr": {
                            "type": "string",
                            "description": "주식 최고가"
                          },
                          "stck_lwpr": {
                            "type": "string",
                            "description": "주식 최저가"
                          },
                          "stck_clpr": {
                            "type": "string",
                            "description": "주식 종가"
                          },
                          "acml_vol": {
                            "type": "string",
                            "description": "누적 거래량"
                          },
                          "prdy_vrss_vol_rate": {
                            "type": "string",
                            "description": "전일 대비 거래량 비율"
                          },
                          "prdy_vrss": {
                            "type": "string",
                            "description": "전일 대비"
                          },
                          "prdy_vrss_sign": {
                            "type": "string",
                            "description": "전일 대비 부호"
                          },
                          "prdy_ctrt": {
                            "type": "string",
                            "description": "전일 대비율"
                          },
                          "hts_frgn_ehrt": {
                            "type": "string",
                            "description": "HTS 외국인 소진율"
                          },
                          "frgn_ntby_qty": {
                            "type": "string",
                            "description": "외국인 순매수 수량"
                          },
                          "flng_cls_code": {
                            "type": "string",
                            "description": "락 구분 코드"
                          },
                          "acml_prtt_rate": {
                            "type": "string",
                            "description": "누적 분할 비율"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## 가이드라인 (API 연동 시 참고사항)

1. **Header 공통 설정**:

   - `content-type`: 반드시 `application/json; charset=utf-8`로 설정해야 합니다.
   - `authorization`: OAuth 2.0 Access Token을 `Bearer {token}` 형식으로 입력합니다. (단, 문서 예시에는 `Bearer` 접두사 언급이 없으므로 발급받은 토큰값 자체를 넣는지 확인 필요, 통상적으로는 Bearer 사용)
   - `appkey` / `appsecret`: KIS 개발자 센터에서 발급받은 키를 사용합니다. 보안에 유의하세요.
   - `tr_id`: 각 API마다 고유한 거래 ID(예: `FHKST03010100`)가 존재하며, 실전/모의투자에 따라 ID가 같거나 다를 수 있으니 문서의 `tr_id` 값을 정확히 매핑해야 합니다.

2. **Query Parameter 값 설정**:

   - `FID_COND_MRKT_DIV_CODE`: 대부분의 주식/ETF 조회 시 국내 주식 시장을 뜻하는 `'J'` 값을 사용합니다.
   - `FID_PERIOD_DIV_CODE`: 기간별 시세 조회 시 `D`(일), `W`(주), `M`(월), `Y`(년) 중 하나를 선택합니다.
   - `FID_ORG_ADJ_PRC`: 차트 분석 시 액면분할 등이 반영된 수정주가를 보려면 `0`, 원주가를 보려면 `1`을 설정합니다.

3. **Response 데이터 처리**:

   - 대부분의 숫자 데이터(가격, 거래량 등)가 JSON 응답에서 `String` 타입으로 반환됩니다. 연산이 필요한 경우 클라이언트 단에서 반드시 숫자형(Integer/Float)으로 변환 후 사용해야 합니다.
   - `rt_cd`가 `0`이면 성공, 그 외의 값은 실패를 의미합니다. 실패 시 `msg1`에 에러 메시지가 포함됩니다.

4. **법인/개인 구분**:

   - Header의 `custtype` 파라미터에 법인은 `B`, 개인은 `P`를 입력해야 하며, 법인의 경우 추가적인 Header(`seq_no`, `mac_address`, `phone_number` 등)가 필수일 수 있습니다. (위 명세는 개인 고객 기준으로 `required` 여부를 작성하였으므로 법인 연동 시 문서의 '법인 필수' 항목을 추가로 확인 바랍니다.)

---

### 5\. 데이터 분석 및 지표 산출 가이드 (Implementation Guide)

위에서 정의한 4가지 API를 활용하여 21가지 핵심 지표를 산출하는 구체적인 방법입니다.

#### 5-1. 기본 정보 및 스냅샷 지표 (실시간/1회 호출)

> **사용 API:** `1. ETF/ETN 현재가` (/uapi/etfetn/v1/quotations/inquire-price)
> **TR_ID:** `FHPST02400000`

이 API는 루프를 돌릴 필요 없이, 분석 시점에 **1회 호출**하여 아래 값들을 그대로 저장하면 됩니다.

| 지표 번호 | 지표명             | API 필드명       | 설명 및 처리 방법                                             |
| :-------- | :----------------- | :--------------- | :------------------------------------------------------------ |
| **3**     | **거래량**         | `acml_vol`       | 누적 거래량. 정수형(`int`) 변환 필수.                         |
| **4**     | **추적 오차**      | `trc_errt`       | 추적오차율(%). 실수형(`float`) 변환.                          |
| **5**     | **NAV**            | `nav`            | 순자산가치. 실수형(`float`) 변환.                             |
| **6**     | **괴리율**         | `dprt`           | (시장가 - NAV) / NAV. 실수형(`float`) 변환.                   |
| **7**     | **설정일**         | `stck_lstn_date` | 상장일을 설정일로 간주. `YYYYMMDD` 형식을 Date 타입으로 변환. |
| **8**     | **운용 규모(AUM)** | `etf_ntas_ttam`  | ETF 순자산총액(억 원 단위 확인 필요). 정수형 변환.            |

---

#### 5-2. 포트폴리오 구성 및 스타일 분석 (배치/1일 1회)

> **사용 API:** `2. ETF 구성종목시세` + `4. 주식기본조회` > **TR_ID:** `FHKST121600C0` (구성종목), `CTPF1002R` (주식기본)

ETF 내부를 분석하기 위해 두 API를 결합(Join)해서 사용해야 합니다.

**Step 1. 구성종목 가져오기 (`2. ETF 구성종목시세`)**

- **지표 9 (상위 종목 & 집중도):**

  - 응답의 `output2` 리스트를 순회합니다.
  - `etf_vltn_amt` (평가금액) 기준으로 내림차순 정렬합니다.
  - 상위 10개 종목의 `etf_vltn_amt` 합계 / 전체 `etf_vltn_amt` 합계 = **상위 10개 집중도(%)**

- **지표 14 (회전율):**

  - **필수 요건:** 전날 저장해둔 구성종목 데이터(Old)가 있어야 합니다.
  - **로직:** `Turnover = Sum(|Today_Weight_i - Yesterday_Weight_i|) / 2`
  - API에서 직접 비중을 주지 않을 경우, `Weight = 개별종목_평가금액 / 전체_평가금액_합`으로 계산하여 사용합니다.

**Step 2. 섹터 및 시총 규모 분석 (`4. 주식기본조회` 결합)**

- API 2에서 얻은 종목코드(`stck_shrn_iscd`)를 API 4의 `PDNO` 파라미터에 넣어 호출합니다.
- **지표 10 (섹터별 분포):** 리턴된 `std_idst_clsf_cd_name`(표준산업분류명)을 기준으로 GroupBy 하여 비중을 합산합니다.
- **지표 12 (시가총액별 분포):**
  - 개별 시총 계산: API 2의 `stck_prpr`(현재가) × API 4의 `lstg_stqt`(상장주수)
  - 계산된 시총을 기준으로 대형/중형/소형으로 분류(예: 코스피 시총 순위 기준)하여 비중을 합산합니다.

---

#### 5-3. 퀀트/리스크 지표 (과거 데이터 연산)

> **사용 API:** `3. 국내주식기간별시세` (/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice)
> **TR_ID:** `FHKST03010100`

가장 연산이 많이 필요한 부분입니다. **최소 1년(약 250거래일)** 치 데이터를 수집해야 신뢰도 있는 지표가 나옵니다.

**[호출 파라미터 설정]**

- `FID_PERIOD_DIV_CODE`: **"D"** (일봉)
- `FID_ORG_ADJ_PRC`: **"0"** (수정주가 사용 필수 - 배당락/액면분할 보정)
- `FID_INPUT_DATE_1` \~ `2`: 최근 1년\~3년 기간 설정

**[지표 산출 로직]**

| 지표 번호  | 지표명                | 계산 방법 (Python Pandas 기준)                                                                                                                                   |
| :--------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **15**     | **수익률**            | `df['close'].pct_change()` 로 일간 수익률(`daily_ret`) 생성 후, 기간별 누적 곱(`prod`) 계산.                                                                     |
| **13**     | **스타일(가치/성장)** | `output1`에 있는 `per`, `pbr` 값을 사용. (PER가 낮으면 가치주, 높으면 성장주 성향으로 판단)                                                                      |
| **16**     | **변동성**            | `daily_ret.std() * sqrt(252)` (연환산 표준편차)                                                                                                                  |
| **17**     | **MDD**               | `(price / price.cummax() - 1).min()` (전고점 대비 최대 낙폭)                                                                                                     |
| **18**     | **샤프 지수**         | `(mean(daily_ret) * 252 - 무위험이자율) / (std(daily_ret) * sqrt(252))`                                                                                          |
| **19**     | **소르티노**          | `(mean(daily_ret) * 252 - 무위험이자율) / (std(daily_ret[daily_ret<0]) * sqrt(252))`                                                                             |
| **20, 21** | **베타, 알파**        | 시장지수(예: KOSPI - 종목코드 `000020` 등)의 일봉 데이터도 동일 기간 호출하여 비교.<br>`Cov(ETF, Market) / Var(Market)` 로 베타 산출 후 CAPM 공식으로 알파 도출. |

---

### 6\. 개발 시 주의사항 (Rate Limit & Data Type)

1. **데이터 타입 변환:** API 응답의 모든 숫자는 \*\*String(문자열)\*\*입니다. 계산 전 반드시 `int()` 또는 `float()`로 변환해야 합니다.
2. **API 호출 제한(Throttling):**
   - `구성종목시세`나 `기간별시세`는 반복 호출이 필요할 수 있습니다.
   - 한국투자증권 API는 초당 호출 제한(약 초당 20건 등, 계좌 등급별 상이)이 있으므로 `time.sleep(0.05)` 등을 주어 호출 간격을 조절해야 합니다.
3. **벤치마크 데이터:** 베타/알파 계산을 위해서는 타겟 ETF뿐만 아니라 **시장 지수(KOSPI/KOSDAQ)** 데이터도 `기간별시세` API로 함께 수집해야 합니다.

```

```
