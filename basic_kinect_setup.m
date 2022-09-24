clear; close all;clc
% The Kinect for Windows Sensor shows up as two separate devices in IMAQHWINFO.
hwInfo = imaqhwinfo('kinect')

hwInfo.DeviceInfo(1)

hwInfo.DeviceInfo(2)

% Create the VIDEOINPUT objects for the two streams
colorVid = videoinput('kinect',1)
depthVid = videoinput('kinect',2)
% Set the triggering mode to 'manual'
triggerconfig([colorVid depthVid],'manual');
colorVid.FramesPerTrigger = 100;
depthVid.FramesPerTrigger = 100;
% Start the color and depth device. This begins acquisition, but does not
% start logging of acquired data.
start([colorVid depthVid]);
% Trigger the devices to start logging of data.
trigger([colorVid depthVid]);
% Retrieve the acquired data
[colorFrameData,colorTimeData,colorMetaData] = getdata(colorVid);
[depthFrameData,depthTimeData,depthMetaData] = getdata(depthVid);
% Stop the devices
stop([colorVid depthVid]);
% Get the VIDEOSOURCE object from the depth device's VIDEOINPUT object.
depthSrc = getselectedsource(depthVid)
% Turn on skeletal tracking.
depthSrc.TrackingMode = 'Skeleton';
% Acquire 100 frames with tracking turned on.
% Remember to have a person in person in front of the
% Kinect for Windows to see valid tracking data.
colorVid.FramesPerTrigger = 100;
depthVid.FramesPerTrigger = 100;
start([colorVid depthVid]);
trigger([colorVid depthVid]);
% Retrieve the frames and check if any Skeletons are tracked
[frameDataColor] = getdata(colorVid);
[frameDataDepth, timeDataDepth, metaDataDepth] = getdata(depthVid);
% Check for tracked skeletons from depth metadata
anyPositionsTracked = any(metaDataDepth(95).IsPositionTracked ~= 0)
anySkeletonsTracked = any(metaDataDepth(95).IsSkeletonTracked ~= 0)

% See which skeletons were tracked.
trackedSkeletons = find(metaDataDepth(95).IsSkeletonTracked)
jointCoordinates = metaDataDepth(95).JointWorldCoordinates(:, :, trackedSkeletons)
% Skeleton's joint indices with respect to the color image
jointIndices = metaDataDepth(95).JointImageIndices(:, :, trackedSkeletons)

% Pull out the 95th color frame
image = frameDataColor(:, :, :, 95);

% Find number of Skeletons tracked
nSkeleton = length(trackedSkeletons);

% Plot the skeleton
util_skeletonViewer(jointIndices, image, nSkeleton);
