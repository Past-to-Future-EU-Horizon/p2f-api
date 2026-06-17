from p2f_api.service.harm_timeslice import create_new_timeslice
from p2f_pydantic.harm_timeslices import HARM_Timeslice

timeslices = [
    HARM_Timeslice("last 7,500 Years", timeslice_age_oldest=7_500, timeslice_age_recent=0),
    HARM_Timeslice("4,2 aridification event", timeslice_age_mean=4_200),
    HARM_Timeslice("Mid-Holocene Warm Period/ Holocene Climatic Optimum", timeslice_age_oldest=9_500, timeslice_age_recent=5_500),
    HARM_Timeslice("Mid-Holocene 6ka", timeslice_age_mean=6_000),
    HARM_Timeslice("thermal maximum of the Holocene Climatic Maximum", timeslice_age_mean=8_000),
    HARM_Timeslice("8,2 Ka cold event", timeslice_age_mean=8_200),
    HARM_Timeslice("Holocene", timeslice_age_oldest=11_700, timeslice_age_recent=0),
    HARM_Timeslice("Bølling-Allerød transition", timeslice_age_oldest=14_600, timeslice_age_recent=13_000),
    HARM_Timeslice("Last glacial-interglacial transition (Termination 1, T1)", timeslice_age_oldest=19_000, timeslice_age_recent=8_000),
    HARM_Timeslice("Last Glacial Maximum (LGM)", timeslice_age_oldest=31_000, timeslice_age_recent=16_000),
    HARM_Timeslice("Last Glacial Maximum (LGM) snapshot", timeslice_age_oldest=23_000, timeslice_age_recent=19_000),
    HARM_Timeslice("Last Glacial Period (LGP)", timeslice_age_oldest=115_000, timeslice_age_recent=11_700),
    HARM_Timeslice("Dansgaard-Oeschger (D-O) events", timeslice_age_oldest=130_000, timeslice_age_recent=11_700),
    HARM_Timeslice("Last interglacial to glacial transition (MIS 5a to MIS 4)", timeslice_age_oldest=85_000, timeslice_age_recent=65_000),
    HARM_Timeslice("Last Interglacial/Eemian/MIS 5e", timeslice_age_oldest=130_000, timeslice_age_recent=115_000),
    HARM_Timeslice("Marine Isotope Stage 5/MIS 5", timeslice_age_oldest=130_000, timeslice_age_recent=80_000),
    HARM_Timeslice("Penultimate glacial-interglacial transition (T2)", timeslice_age_oldest=140_000, timeslice_age_recent=120_000),
    HARM_Timeslice("Penultimate interglacial to glacial transition (MIS 7e to MIS 7d)", timeslice_age_oldest=250_000, timeslice_age_recent=225_000),
    HARM_Timeslice("Marine Isotope Stage 11/MIS 11", timeslice_age_oldest=424_000, timeslice_age_recent=374_000),
    HARM_Timeslice("Mid-Pleistocene Transition/MPT", timeslice_age_oldest=1_250_000, timeslice_age_recent=700_000),
    # HARM_Timeslice("late Pliocene and early Pleistocene glacial-interglacial cycles", timeslice_age_oldest=, timeslice_age_recent=), # No dates provided in spreadsheet 
    HARM_Timeslice("Pre-MPT glacial cycles (MIS 39 to MIS 45)", timeslice_age_oldest=1_400_000, timeslice_age_recent=1_250_000),
    HARM_Timeslice("MIS 100 (MIS 95 to MIS 101)", timeslice_age_oldest=2_600_000, timeslice_age_recent=2_400_000),
    HARM_Timeslice("Pliocene-Pleistocene transition", timeslice_age_mean=2_580_000),
    HARM_Timeslice("Pliocene", timeslice_age_oldest=5_330_000, timeslice_age_recent=2_580_000),
    HARM_Timeslice("Mid-Piacenzian Warm Period (mPWP)/Mid-Pliocene Warm Period", timeslice_age_oldest=3_300_000, timeslice_age_recent=3_000_000),
    HARM_Timeslice("KM5c interglacial", timeslice_age_mean=3_205_000),
    # HARM_Timeslice("KM5c-M2 transition", timeslice_age_oldest=, timeslice_age_recent=), # No dates provided in spreadsheet
    HARM_Timeslice("M2 glacial", timeslice_age_mean=3_300_000),
    HARM_Timeslice("Eocene Climatic Optimum/Early Eocene Climatic Optimum/EECO", timeslice_age_oldest=53_000_000, timeslice_age_recent=49_000_000),
]
for timeslice in timeslices:
    create_new_timeslice(new_harm_timeslice=HARM_Timeslice)