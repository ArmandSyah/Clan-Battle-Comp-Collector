import React from "react";
import { Dialog } from "@headlessui/react";
import { useDeleteTeamCompMutation } from "../../app/api/apiSlice";
import AddingTeamComp from "../../components/Gif/AddingTeamComp";
import { useNavigate } from "react-router-dom";

export default function DeleteModal({
  teamCompId,
  deleteModalIsOpen,
  closeModal,
}) {
  const [
    deleteTeamComp,
    { isLoading: deletingTeamComp, isSuccess: teamCompDeleted },
  ] = useDeleteTeamCompMutation();
  const navigate = useNavigate();

  const onYesClicked = async () => {
    try {
      await deleteTeamComp(teamCompId).unwrap();
    } catch (err) {
      console.log("Failed to delete team comp: ", err);
    }
  };

  if (deletingTeamComp) {
    return (
      <div className="absolute top-2/4 left-2/4">
        <AddingTeamComp />
      </div>
    );
  } else if (teamCompDeleted) {
    console.log("Team comp has deleted");
    return navigate("/clanBattle");
  }

  return (
    <Dialog
      open={deleteModalIsOpen}
      onClose={closeModal}
      className="absolute z-10"
    >
      {/* The backdrop, rendered as a fixed sibling to the panel container */}
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      {/* Full-screen scrollable container */}
      <div className="fixed inset-0 flex items-center justify-center p-4">
        {/* Container to center the panel */}
        <div className="flex h-auto w-auto items-center justify-center">
          <Dialog.Panel className="max-h-96 w-full max-w-md rounded bg-gradient-to-r from-slate-500 to-slate-800 p-12 overflow-y-auto">
            <Dialog.Title
              as="h2"
              className="flex justify-between text-2xl font-bold leading-6 text-stone-100"
            >
              <span>Deleting a Team Comp</span>
            </Dialog.Title>
            <div className="flex flex-col mt-4 gap-4">
              <p className="text-sm text-stone-100">
                Are you sure you want to delete this team comp
              </p>
              <div className="flex gap-4">
                <button
                  onClick={onYesClicked}
                  type="button"
                  className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                >
                  Yes
                </button>
                <button
                  type="button"
                  className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  onClick={closeModal}
                >
                  No
                </button>
              </div>
            </div>
          </Dialog.Panel>
        </div>
      </div>
    </Dialog>
  );
}
