import streamlit as st
from recommender import semantic_keyword_search, get_semantic_recommendations
import pandas as pd

st.set_page_config(page_title="Berkeley Course Compass", layout="wide")
st.title("🎓 Berkeley Course Compass")
st.markdown("Discover similar or relevant courses using semantic search and natural language understanding.")

mode = st.radio("Choose a mode:", ["🔍 Search by Keyword", "📚 Recommend Similar Courses"])

departments = ['', 'A,RESEC', 'AEROENG', 'AEROSPC', 'AFRICAM', 'AGRS', 'AHMA', 'AMERSTD', 'ANTHRO', 'ARABIC', 'ARCH', 'ARMENI', 'ART', 'ASAMST', 'ASIANST', 'AST', 'ASTRON', 'BANGLA', 'BIOLOGY', 'BIOPHY', 'BIO_ENG', 'BOSCRSR', 'BUDDSTD', 'BULGARI', 'BURMESE', 'CATALAN', 'CDSS', 'CELTIC', 'CHEM', 'CHICANO', 'CHINESE', 'CHM_ENG', 'CIV_ENG', 'CLASSIC', 'CMPBIO', 'COG_SCI', 'COLWRIT', 'COMPBIO', 'COMPSCI', 'COMPSS', 'COM_LIT', 'CPH', 'CRIT_TH', 'CRWRIT', 'CUNEIF', 'CYBER', 'CY_PLAN', 'CZECH', 'DANISH', 'DATA', 'DATASCI', 'DEMOG', 'DES_INV', 'DEVP', 'DEV_ENG', 'DEV_STD', 'DIGHUM', 'DUTCH', 'EA_LANG', 'ECON', 'EDSTEM', 'EDUC', 'EECS', 'EGYPT', 'EL_ENG', 'ENE,RES', 'ENGIN', 'ENGLISH', 'ENVECON', 'ENV_DES', 'EPS', 'ESPM', 'ETH_STD', 'EUST', 'EWMBA', 'FILIPN', 'FILM', 'FINNISH', 'FOLKLOR', 'FPF', 'FRENCH', 'GEOG', 'GERMAN', 'GLOBAL', 'GMS', 'GPP', 'GREEK', 'GSPDP', 'GWS', 'HEBREW', 'HINDI', 'HISTART', 'HISTORY', 'HMEDSCI', 'HUM', 'HUNGARI', 'IAS', 'ICELAND', 'INDONES', 'IND_ENG', 'INFO', 'INTEGBI', 'IRANIAN', 'ISF', 'ITALIAN', 'JAPAN', 'JEWISH', 'JOURN', 'KHMER', 'KOREAN', 'LAN_PRO', 'LATAMST', 'LATIN', 'LD_ARCH', 'LEGALST', 'LGBT', 'LINGUIS', 'L_S', 'MATH', 'MAT_SCI', 'MBA', 'MCELLBI', 'MEC_ENG', 'MEDIAST', 'MED_ST', 'MELC', 'MFE', 'MIL_AFF', 'MIL_SCI', 'MONGOLN', 'MPS', 'MUSIC', 'M_E_STU', 'NATAMST', 'NAT_RES', 'NAV_SCI', 'NEU', 'NORWEGN', 'NSE', 'NUC_ENG', 'NUSCTX', 'NWMEDIA', 'OPTOM', 'PACS', 'PB_HLTH', 'PERSIAN', 'PHDBA', 'PHILOS', 'PHYSICS', 'PHYS_ED', 'PLANTBI', 'POLECON', 'POLISH', 'POL_SCI', 'PORTUG', 'PSYCH', 'PUBAFF', 'PUB_POL', 'PUNJABI', 'RDEV', 'RHETOR', 'RUSSIAN', 'SANSKR', 'SASIAN', 'SCANDIN', 'SCMATHE', 'SEASIAN', 'SEMITIC', 'SLAVIC', 'SOCIOL', 'SOC_WEL', 'SPANISH', 'SSEASN', 'STAT', 'STRELIG', 'STS', 'SWEDISH', 'TAMIL', 'TELUGU', 'THAI', 'THEATER', 'TIBETAN', 'TURKISH', 'UGBA', 'UGIS', 'UKRAINI', 'URDU', 'VIETNMS', 'VIS_SCI', 'VIS_STD', 'XMBA', 'YIDDISH']
department_filter = st.selectbox("Filter by department (optional)", departments)

if mode == "🔍 Search by Keyword":
    query = st.text_input("Enter a topic, skill, or keyword")
    if query:
        results = semantic_keyword_search(query, top_n=100)

        if department_filter:
            results = results[results['course_code'].str.upper().str.startswith(department_filter.upper())]
        results = results.head(10)

        if results.empty:
            st.warning("No good matches found.")
        else:
            st.success(f"Top results for \"{query}\":")
            for _, row in results.iterrows():
                st.markdown(f"**{row['course_code']} — {row['title']}**")
                st.markdown(f"*Score:* {row['score']:.2f}")
                st.markdown(row['description'])
                if 'reason' in row and row['reason']:
                    st.markdown(f"🔍 *Why recommended:* shares topics like _{row['reason']}_.")
                st.markdown("---")

elif mode == "📚 Recommend Similar Courses":
    course_input = st.text_input("Enter a course code (e.g., COMPSCI 61A)")
    if course_input:
        results = get_semantic_recommendations(course_input, top_n=10, department_filter=department_filter or None)
        if isinstance(results, str):
            st.error(results)
        elif results.empty:
            st.warning("No good matches found.")
        else:
            st.success(f"Courses similar to {course_input.upper()}:")
            for _, row in results.iterrows():
                st.markdown(f"**{row['course_code']} — {row['title']}**")
                st.markdown(f"*Score:* {row['score']:.2f}")
                st.markdown(row['description'])
                if 'reason' in row and row['reason']:
                    st.markdown(f"🔍 *Why recommended:* shares topics like _{row['reason']}_.")
                st.markdown("---")
